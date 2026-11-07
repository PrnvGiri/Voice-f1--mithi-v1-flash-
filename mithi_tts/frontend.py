"""Text front end: Maya text normaliser -> espeak-ng / misaki G2P -> Kokoro phoneme string, plus the words indic-bert
reads and the word index of every phoneme token.

    norm, ps = phonemes("आज मौसम कितना अच्छा है!", "hi")
"""
import json
import os
import re
import unicodedata

from .text_norm import normalize_text

LANGS = {"hi": "Hindi", "en": "English", "bn": "Bengali", "gu": "Gujarati", "kn": "Kannada", "ml": "Malayalam",
         "mr": "Marathi", "or": "Odia", "pa": "Punjabi", "ta": "Tamil", "te": "Telugu"}

# Kokoro-82M phoneme vocabulary (char -> id) plus the breath token the writer inserts (id 7, never emitted by G2P)
VOCAB = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vocab.json"), encoding="utf-8"))
BREATH, BREATH_ID = "⁂", 7
VOCAB = {**VOCAB, BREATH: BREATH_ID}

NUKTA = "़"
PUNCT = ',.!?;:—…"“”()'
SPLIT_PUNCT = re.compile(r"([,.!?;:—…\"“”()])")
LATIN_RUN = re.compile(r"([A-Za-z][A-Za-z']*(?:\s+[A-Za-z][A-Za-z']*)*)")
# espeak-ng phones some Indic languages use that Kokoro's vocabulary lacks -> the closest Kokoro phone
IPA_ALIASES = {"ɭ": "l", "ʉ": "u", "̩": "", "+": ""}
PAUSE_IDS = {VOCAB[c] for c in " ,.!?;:—…" if c in VOCAB}
SPACE = VOCAB[" "]
PUNCT_IDS = {VOCAB[c] for c in PUNCT if c in VOCAB}

# ---------------------------------------------------------------- G2P
_g2p = {}


def _short_espeak_path():
    """espeak-ng cannot open a data folder whose path is longer than about 160 characters (deep virtualenvs). In that
    case copy the data (19 MB, once) to a short folder and point espeak there."""
    try:
        import shutil
        import tempfile
        import espeakng_loader
        from phonemizer.backend.espeak.wrapper import EspeakWrapper
        data = espeakng_loader.get_data_path()
        if len(data) < 140:
            return
        for base in (os.path.expanduser("~/.cache/mithi"), os.path.join(tempfile.gettempdir(), "mithi")):
            short = os.path.join(base, "espeak-ng-data")
            if len(short) >= 140:
                continue
            try:
                if not os.path.exists(os.path.join(short, "phontab")):
                    os.makedirs(base, exist_ok=True)
                    tmp = short + f".tmp{os.getpid()}"
                    shutil.copytree(data, tmp)
                    os.replace(tmp, short)
            except OSError:
                continue
            EspeakWrapper.set_data_path(short)
            return
    except Exception:
        pass


def _init_g2p(lang):
    from misaki import en, espeak
    _short_espeak_path()
    if lang not in LANGS:
        raise ValueError(f"unsupported language: {lang} (one of {', '.join(LANGS)})")
    if lang != "en":
        _g2p[lang] = espeak.EspeakG2P(language=lang)
    _g2p["en"] = en.G2P(trf=False, british=False, fallback=espeak.EspeakFallback(british=False))


def restore_nukta(text, text_norm):
    """The Maya normaliser drops the nukta (पेड़ -> पेड); put it back wherever the original word had one."""
    nfd = lambda w: unicodedata.normalize("NFD", w)  # noqa: E731
    table = {}
    for w in re.findall(r"[ऀ-ॿ]+", text):
        if NUKTA in nfd(w):
            table[unicodedata.normalize("NFC", nfd(w).replace(NUKTA, ""))] = unicodedata.normalize("NFC", w)
    if not table:
        return text_norm
    return re.sub(r"[ऀ-ॿ]+", lambda m: table.get(m.group(), m.group()), text_norm)


# Legacy-font typing leaves two vowel signs in a row (छाेटा, काॅक्स); espeak-ng crashes on some of them.
MATRA_FIX = [("ाॅ", "ॉ"), ("ॅा", "ॉ"), ("ाे", "ो"), ("ेा", "ो"), ("ाै", "ौ"), ("ैा", "ौ")]
DOUBLE_SIGN = re.compile(r"([ा-ौ])[ा-ौ]+")


def fix_matras(t):
    for bad, good in MATRA_FIX:
        t = t.replace(bad, good)
    return DOUBLE_SIGN.sub(r"\1", t)


def _phonemize_hi(chunk):
    chunk = re.sub(r"['\-–]+", " ", chunk).strip()        # espeak-ng hi crashes on a run starting with "'-"
    if not chunk:
        return ""
    ps = _g2p["hi"](chunk)[0]
    # espeak-ng hi writes ड़/ढ़ as "r."; inside a punctuation-free chunk any "." is that marker
    return ps.replace("r.", "ɽ").replace(".", "")


def _phonemize(text, text_norm, lang):
    t = restore_nukta(text, text_norm) if lang in ("hi", "mr") else text_norm
    if lang in ("hi", "mr"):
        t = fix_matras(t)
    t = t.replace("।", ".").replace("॥", ".")
    t = re.sub(r"(?<=\w)-(?=\w)", " ", t)
    out = ""
    for piece in SPLIT_PUNCT.split(t):
        if not piece:
            continue
        if piece in PUNCT:
            out = out.rstrip() + piece + " "
            continue
        words = []
        for run in LATIN_RUN.split(piece):
            run = run.strip()
            if not run:
                continue
            if LATIN_RUN.fullmatch(run):
                words.append(_g2p["en"](run)[0])
            elif lang == "hi":
                words.append(_phonemize_hi(run))
            else:
                words.append(_g2p[lang](run)[0])
        if words:
            out += " ".join(w for w in words if w) + " "
    out = re.sub(r"\s+", " ", out).strip()
    for old, new in IPA_ALIASES.items():
        out = out.replace(old, new)
    return "".join(c for c in out if c in VOCAB)


def phonemes(text, lang):
    """text -> (normalised text, Kokoro phoneme string)."""
    if lang not in _g2p:
        _init_g2p(lang)
    norm = normalize_text(text, lang)
    return norm, _phonemize(text, norm, lang)


# ---------------------------------------------------------------- words for indic-bert
def words_of(text, text_norm):
    """The words the meaning encoder reads (same transformations as _phonemize), punctuation attached to the word
    before it. The n-th space-separated phoneme group is the n-th word."""
    t = fix_matras(restore_nukta(text, text_norm)).replace("।", ".").replace("॥", ".")
    t = re.sub(r"(?<=\w)-(?=\w)", " ", t)
    t = re.sub(r"['\-–]+", " ", t)
    out = ""
    for piece in SPLIT_PUNCT.split(t):
        if not piece:
            continue
        out = out.rstrip() + piece + " " if piece in PUNCT else out + piece.strip() + " "
    words = []
    for g in (w for w in re.sub(r"\s+", " ", out).split(" ") if w):
        if all(c in PUNCT for c in g):          # a punctuation-only group joins the word before it
            if words:
                words[-1] += g
        else:
            words.append(g)
    return words


def token_words(ids):
    """Word index per token (BOS/EOS and spaces -1, punctuation / breath -> the word before) and the word count."""
    out, w, in_word, last = [], -1, False, -1
    for k, t in enumerate(ids):
        if k == 0 or k == len(ids) - 1 or t == SPACE:
            out.append(-1)
            in_word = False
        elif t == BREATH_ID or t in PUNCT_IDS:
            out.append(last)
        else:
            if not in_word:
                w += 1
                in_word = True
            out.append(w)
            last = w
    return out, w + 1


# ---------------------------------------------------------------- long text
def split_text(text, lang, limit=400):
    """The whole text if its phonemes fit, else sentences (and, if still too long, comma pieces) under the limit.
    Odia ୱ is written ବ (espeak-ng spells ୱ words letter by letter)."""
    text = " ".join(text.split())
    if lang == "or":
        text = text.replace("ୱ", "ବ")
    if len(phonemes(text, lang)[1]) <= limit:
        return [text]
    parts = [s.strip() for s in re.split(r"(?<=[.!?।॥])\s+", text) if s.strip()]
    out = []
    for s in parts:
        if len(phonemes(s, lang)[1]) <= limit:
            out.append(s)
            continue
        cur = ""
        for piece in re.split(r"(?<=[,;:])\s+", s):
            if cur and len(phonemes(cur + " " + piece, lang)[1]) > limit:
                out.append(cur)
                cur = piece
            else:
                cur = (cur + " " + piece).strip()
        if cur:
            out.append(cur)
    return out
