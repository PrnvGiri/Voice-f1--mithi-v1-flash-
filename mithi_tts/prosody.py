"""Prosody writer: reads a sentence (phoneme tokens + indic-bert word meaning + speaker + language) and writes Maya-style
prosody one phoneme token at a time, as discrete codes; decode() turns the codes into the per-token durations and the
frame-level F0 / energy the Kokoro decoder takes (2 frames per 25 ms unit).

Codes per token (P5): dur, uv0, uv1, p1..p5 (pitch, 0.5-semitone bins re 100 Hz), e1..e3 (energy, 0.25 bins),
then breath_next (1 = the writer inserts a breath token after this one).
The writer predicts voicing explicitly and pitch / energy as changes from the previous point (v2 design), and its depth
heads predict the codes of one token in order, each seeing the ones before it.
"""
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from .frontend import BREATH_ID

# ---------------------------------------------------------------- code tables
DUR_MAX, UV_MAX = 63, 31
ST_LO, ST_STEP, N_ST = -10.0, 0.5, 81            # -10 .. +30 semitones
PITCH_NONE = N_ST                                # extra class: no voiced frame
E_LO, E_STEP, N_E = -6.0, 0.25, 65               # -6 .. +10
K_PITCH, J_ENERGY = 5, 3                         # P5: 5 pitch + 3 energy points
P5_COLS = 3 + K_PITCH + J_ENERGY                 # 11 = index of breath_next in what sample() returns


def _interp(points, n):
    """n frame values through k points placed at the centres of k equal parts."""
    k = len(points)
    if n == 0:
        return np.zeros(0)
    pos = (np.arange(k) + 0.5) / k * n - 0.5
    return np.interp(np.arange(n), pos, points)


def decode(codes):
    """P5 codes [T, 11] -> dur [T] units, f0 [2*sum(dur)] Hz, energy [2*sum(dur)]."""
    k = K_PITCH
    dur = codes[:, 0].astype(np.int64)
    n = 2 * int(dur.sum())
    f0, en, s = np.zeros(n, np.float32), np.zeros(n, np.float32), 0
    for t, d in enumerate(dur):
        if d == 0:
            continue
        a, b = 2 * s, 2 * (s + d)
        s += d
        en[a:b] = _interp(E_LO + E_STEP * codes[t, 3 + k:].astype(np.float64), b - a)
        p = codes[t, 3:3 + k]
        if (p == PITCH_NONE).any():
            continue
        v0, v1 = a + min(int(codes[t, 1]), b - a), b - min(int(codes[t, 2]), b - a)
        if v1 > v0:
            st = _interp(ST_LO + ST_STEP * p.astype(np.float64), v1 - v0)
            f0[v0:v1] = 100 * 2 ** (st / 12)
    return dur, f0, en


# ---------------------------------------------------------------- writer
NAMES = ["dur", "voiced", "uv0", "uv1", "d1", "d2", "d3", "d4", "d5", "f1", "f2", "f3", "breath"]
WRITER_LANGS = ["hi", "en", "bn", "gu", "kn", "ml", "mr", "or", "pa", "ta", "te", "as"]
D_P, D_E = 80, 64
REF_P = int(round((0 - ST_LO) / ST_STEP))           # 0 st re 100 Hz: the reference before the first voiced token
REF_E = int(round((0 - E_LO) / E_STEP))
ABS_CLASSES = [DUR_MAX + 1, 2, UV_MAX + 1, UV_MAX + 1] + [N_ST + 1] * 5 + [N_E] * 3 + [2]
REL_CLASSES = [DUR_MAX + 1, 2, UV_MAX + 1, UV_MAX + 1] + [2 * D_P + 1] * 5 + [2 * D_E + 1] * 3 + [2]
VOICED, BREATH_NEXT = 1, 12                         # columns of the 13-column absolute layout


def abs_to_p5(codes_abs):
    """absolute layout [N, 13] -> (P5 codes [N, 11], breath_next [N])."""
    return torch.cat([codes_abs[:, :1], codes_abs[:, 2:12]], 1), codes_abs[:, BREATH_NEXT]


class ProsodyWriter(nn.Module):
    def __init__(self, n_tok=178, word_dim=768, d=384, heads=6, enc_layers=4, dec_layers=4, n_spk=2,
                 n_lang=len(WRITER_LANGS), depth_hid=256, dropout=0.1):
        super().__init__()
        self.d = d
        self.tok = nn.Embedding(n_tok, d)
        self.word = nn.Linear(word_dim, d)
        self.no_word = nn.Parameter(torch.zeros(d))
        self.spk = nn.Embedding(n_spk, d)
        self.lang = nn.Embedding(n_lang, d)
        self.enc_pos = nn.Conv1d(d, d, 7, padding=3, groups=d)
        self.enc = nn.TransformerEncoder(nn.TransformerEncoderLayer(d, heads, 4 * d, dropout, batch_first=True, norm_first=True),
                                         enc_layers, enable_nested_tensor=False)
        self.enc_norm = nn.LayerNorm(d)
        self.code_emb = nn.ModuleList([nn.Embedding(c, d) for c in ABS_CLASSES])
        self.start = nn.Parameter(torch.zeros(d))
        self.dec = nn.TransformerDecoder(nn.TransformerDecoderLayer(d, heads, 4 * d, dropout, batch_first=True, norm_first=True),
                                         dec_layers)
        self.dec_norm = nn.LayerNorm(d)
        self.depth = nn.ModuleList([nn.Sequential(nn.Linear(d, depth_hid), nn.GELU(), nn.Linear(depth_hid, c)) for c in REL_CLASSES])

    def read(self, enc_ids, word_vec, has_word, spk, lang, enc_pad):
        x = (self.tok(enc_ids) + torch.where(has_word[..., None], self.word(word_vec), self.no_word)
             + (self.spk(spk) + self.lang(lang))[:, None])
        x = x.masked_fill(enc_pad[..., None], 0)
        x = x + self.enc_pos(x.transpose(1, 2)).transpose(1, 2)
        return self.enc_norm(self.enc(x, src_key_padding_mask=enc_pad))

    def _prev_codes(self, ctx):
        e = sum(emb(ctx[..., k]) for k, emb in enumerate(self.code_emb))
        return torch.cat([self.start.expand(ctx.shape[0], 1, self.d), e[:, :-1]], 1)

    def write(self, H, enc_pad, dec_ids, dec_map, ctx, dec_pad):
        x = torch.gather(H, 1, dec_map[..., None].expand(-1, -1, self.d)) + self.tok(dec_ids) + self._prev_codes(ctx)
        causal = torch.triu(torch.ones(x.shape[1], x.shape[1], dtype=torch.bool, device=x.device), 1)
        h = self.dec(x, H, tgt_mask=causal, tgt_key_padding_mask=dec_pad, memory_key_padding_mask=enc_pad, tgt_is_causal=True)
        return self.dec_norm(h)

    @staticmethod
    def _abs_from_rel(k, c, abs_row, prev_p5, prev_e3):
        if k == 4:
            return (prev_p5 + c - D_P).clamp(0, N_ST - 1)
        if 5 <= k <= 8:
            return (abs_row[k - 1] + c - D_P).clamp(0, N_ST - 1)
        if k == 9:
            return (prev_e3 + c - D_E).clamp(0, N_E - 1)
        if 10 <= k <= 11:
            return (abs_row[k - 1] + c - D_E).clamp(0, N_E - 1)
        return c

    @torch.no_grad()
    def sample(self, H, enc_ids, pause_ids, temp=0.8, top_p=0.9, max_breaths=None, head_temp=None):
        """Write one sentence (batch of 1), token by token. head_temp = {code name: temperature} (0 = most likely).
        Returns (dec_ids [Nd] incl. inserted breaths, P5 codes + breath_next [Nd, 12])."""
        dev = H.device
        dec_ids, dec_map, rows = [], [], []
        enc_pad = torch.zeros(1, H.shape[1], dtype=torch.bool, device=dev)
        queue = [(int(t), i) for i, t in enumerate(enc_ids.tolist())]
        n_breath, prev_p5, prev_e3 = 0, REF_P, REF_E
        while queue:
            tok, i = queue.pop(0)
            dec_ids.append(tok)
            dec_map.append(i)
            ctx = torch.tensor(rows + [[0] * len(NAMES)], device=dev)[None]
            ids = torch.tensor(dec_ids, device=dev)[None]
            h = self.write(H, enc_pad, ids, torch.tensor(dec_map, device=dev)[None], ctx,
                           torch.zeros_like(ids, dtype=torch.bool))[0, -1]
            row, acc = [], h
            for k, head in enumerate(self.depth):
                t = (head_temp or {}).get(NAMES[k], temp)
                if 2 <= k <= 8 and row[VOICED] == 0:
                    a = PITCH_NONE if k >= 4 else 0
                else:
                    c = _sample(head(acc), t, 1.0 if k == BREATH_NEXT else top_p)
                    a = int(self._abs_from_rel(k, torch.tensor(c), torch.tensor(row + [0]), torch.tensor(prev_p5), torch.tensor(prev_e3))) \
                        if 4 <= k <= 11 else c
                if k == BREATH_NEXT and (tok not in pause_ids or tok == BREATH_ID or not queue
                                         or (max_breaths is not None and n_breath >= max_breaths)):
                    a = 0
                row.append(a)
                acc = acc + self.code_emb[k](torch.tensor(a, device=dev))
            rows.append(row)
            if row[VOICED] == 1:
                prev_p5 = row[8]
            prev_e3 = row[11]
            if row[BREATH_NEXT] == 1:
                queue.insert(0, (BREATH_ID, i))
                n_breath += 1
        out = torch.tensor(rows)
        p5, breath = abs_to_p5(out)
        return torch.tensor(dec_ids), torch.cat([p5, breath[:, None]], 1)


def _sample(logits, temp, top_p):
    if temp <= 0:
        return int(logits.argmax())
    p = F.softmax(logits / temp, -1)
    sp, idx = p.sort(descending=True)
    keep = sp.cumsum(-1) - sp < top_p
    sp = sp * keep
    return int(idx[torch.multinomial(sp / sp.sum(), 1)])
