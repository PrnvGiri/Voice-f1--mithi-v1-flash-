"""Mithi text-to-speech: 11 Indian languages, voices Satvik and Charvi.

    text -> Maya text normaliser -> espeak-ng / misaki G2P (Kokoro phonemes)
         -> indic-bert word vectors -> prosody writer (durations, pitch, loudness, breaths per phoneme)
         -> Kokoro text encoder + iSTFTNet decoder -> 24 kHz audio

    from mithi_tts import Mithi
    tts = Mithi("path/to/mithi-v1-flash")          # the downloaded model folder
    audio = tts.synthesize("आज मौसम कितना अच्छा है!", lang="hi", voice="charvi")   # numpy array, 24 kHz
"""
import json
import os

import numpy as np
import torch
import torch.nn as nn
from safetensors import safe_open
from safetensors.torch import load_file

from . import frontend as fe
from .indic_encoder import IndicTextEncoder
from .kokoro.istftnet import Decoder
from .kokoro.modules import TextEncoder
from .prosody import P5_COLS, WRITER_LANGS, ProsodyWriter, decode

SR = 24000
DEFAULT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class KokoroDecoder(nn.Module):
    """The parts of Kokoro-82M this model uses: phoneme text encoder and iSTFTNet decoder."""

    def __init__(self, cfg):
        super().__init__()
        self.text_encoder = TextEncoder(channels=cfg["hidden_dim"], kernel_size=cfg["text_encoder_kernel_size"],
                                        depth=cfg["n_layer"], n_symbols=cfg["n_token"])
        self.decoder = Decoder(dim_in=cfg["hidden_dim"], style_dim=cfg["style_dim"], dim_out=cfg["n_mels"],
                               disable_complex=False, **cfg["istftnet"])


class Mithi:
    LANGS = fe.LANGS

    def __init__(self, model_dir=DEFAULT_DIR, device=None):
        self.dir = model_dir
        self.dev = torch.device(device or ("cuda" if torch.cuda.is_available() else "cpu"))
        torch.backends.cuda.matmul.allow_tf32 = False
        m = os.path.join(model_dir, "model")
        if not os.path.isdir(m):                               # weights at the top of the model folder
            m = model_dir
        self.cfg = json.load(open(os.path.join(model_dir, "config.json"), encoding="utf-8"))
        self.settings = dict(self.cfg["inference"])

        kcfg = json.load(open(os.path.join(m, "kokoro_config.json"), encoding="utf-8"))
        self.vocab = kcfg["vocab"]
        self.kokoro = KokoroDecoder(kcfg)
        self.kokoro.load_state_dict(load_file(os.path.join(m, "decoder.safetensors")))

        with safe_open(os.path.join(m, "writer.safetensors"), "pt") as f:
            meta = f.metadata()
        self.voices = json.loads(meta["voices"])
        self.writer = ProsodyWriter(n_spk=len(self.voices))
        self.writer.load_state_dict(load_file(os.path.join(m, "writer.safetensors")))

        self.text_enc = IndicTextEncoder(os.path.join(m, "indic_encoder"))
        self.kokoro, self.writer, self.text_enc = (x.to(self.dev).eval() for x in (self.kokoro, self.writer, self.text_enc))
        self.packs = {v: t.float().to(self.dev) for v, t in load_file(os.path.join(m, "voices.safetensors")).items()}

    # ------------------------------------------------------------------ one sentence
    @torch.no_grad()
    def synth_sentence(self, text, lang, voice, seed=0):
        s, dev = self.settings, self.dev
        torch.manual_seed(seed)
        norm, ps = fe.phonemes(text, lang)
        ids = torch.LongTensor([0, *[i for i in map(self.vocab.get, ps) if i is not None], 0])
        words = fe.words_of(text, norm)
        tok_word, n_groups = fe.token_words(ids.tolist())
        if n_groups == len(words):
            wv, _ = self.text_enc.word_vectors(" ".join(words))
            tw = torch.tensor(tok_word)
            word_vec, has = wv[tw.clamp(min=0)][None], (tw >= 0)[None].to(dev)
        else:                                               # word / phoneme groups disagree: phonemes only
            word_vec = torch.zeros(1, len(ids), self.text_enc.dim, device=dev)
            has = torch.zeros(1, len(ids), dtype=torch.bool, device=dev)
        x = ids[None].to(dev)
        spk = torch.tensor([self.voices.index(voice)], device=dev)
        H = self.writer.read(x, word_vec, has, spk, torch.tensor([WRITER_LANGS.index(lang)], device=dev),
                             torch.zeros_like(x, dtype=torch.bool))
        head_temp = {k: s["voicing_temp"] for k in ("voiced", "uv0", "uv1")}
        dec_ids, codes = self.writer.sample(H, ids, fe.PAUSE_IDS, temp=s["writer_temp"], top_p=s["writer_top_p"],
                                            head_temp=head_temp)
        codes[[0, -1], 0] = codes[[0, -1], 0].clamp(max=s["edge_max"])      # short silence at both ends
        dur, f0, en = decode(codes[:, :P5_COLS].numpy())
        f0 = f0 * np.float32(2 ** (s["pitch_shift"] / 12))
        y = dec_ids[None].to(dev)
        T = int(dur.sum())
        aln = torch.zeros(1, y.shape[1], T, device=dev)
        aln[0, torch.repeat_interleave(torch.arange(y.shape[1], device=dev), torch.from_numpy(dur).to(dev)),
            torch.arange(T, device=dev)] = 1
        ref = self.packs[voice][min(len(ps), len(self.packs[voice])) - 1]
        h = self.kokoro.text_encoder(y, torch.tensor([y.shape[1]], device=dev), torch.zeros_like(y, dtype=torch.bool)) @ aln
        audio = self.kokoro.decoder(h, torch.from_numpy(f0)[None].to(dev), torch.from_numpy(en)[None].to(dev), ref[:, :128])
        return audio.squeeze().float().cpu().numpy()

    # ------------------------------------------------------------------ any length
    def split(self, text, lang):
        """The pieces synthesize() reads: the whole text, or sentences / comma pieces when it is long."""
        return fe.split_text(text, lang, self.settings["max_phonemes_per_piece"])

    def synthesize(self, text, lang="hi", voice="charvi", seed=None, gap=0.15):
        """Text of any length -> audio at 24 kHz in [-1, 1]. Long text is read sentence by sentence."""
        if lang not in fe.LANGS:
            raise ValueError(f"unknown language {lang} (one of {', '.join(fe.LANGS)})")
        if voice not in self.voices:
            raise ValueError(f"unknown voice {voice} (one of {', '.join(self.voices)})")
        if not text or not text.strip():
            raise ValueError("empty text")
        seed = self.settings["seed"] if seed is None else seed
        silence = np.zeros(int(gap * SR), np.float32)
        segs = []
        for p in self.split(text, lang):
            segs += ([silence] if segs else []) + [self.synth_sentence(p, lang, voice, seed).astype(np.float32)]
        return np.clip(np.concatenate(segs), -1.0, 1.0)

    def save(self, audio, path):
        import soundfile as sf
        sf.write(path, audio, SR, subtype="PCM_16")
