"""Meaning encoder for the prosody writer: ai4bharat/indic-bert (ALBERT) with its word table trimmed to the 105,229
pieces our languages use (21.3 M parameters, outputs identical to the full model).

Preprocessing matches indic-bert's pretraining (ALBERT's preprocess_text): collapse spaces, NFKD, drop combining marks
(in Indic scripts: virama and nukta; vowel signs stay), lowercase. SentencePiece is called directly (the transformers
AlbertTokenizer also strips the vowel signs) and its ids are remapped to the trimmed table.
"""
import unicodedata

import numpy as np
import sentencepiece as spm
import torch
import torch.nn as nn
from transformers import AlbertModel

CLS, SEP = 2, 3


def preprocess(text):
    text = unicodedata.normalize("NFKD", " ".join(text.split()))
    return "".join(c for c in text if not unicodedata.combining(c)).lower()


class IndicTextEncoder(nn.Module):
    def __init__(self, model_dir):
        super().__init__()
        self.sp = spm.SentencePieceProcessor(model_file=f"{model_dir}/spiece.model")
        self.register_buffer("old2new", torch.from_numpy(np.load(f"{model_dir}/old2new.npy")), persistent=False)
        self.bert = AlbertModel.from_pretrained(model_dir, dtype=torch.float32)
        self.dim = self.bert.config.hidden_size

    def pieces(self, words):
        ids, owner = [CLS], [-1]
        for w, word in enumerate(words):
            p = self.sp.encode(preprocess(word))
            ids += p
            owner += [w] * len(p)
        ids.append(SEP)
        owner.append(-1)
        return self.old2new[torch.tensor(ids)], torch.tensor(owner)

    def word_vectors(self, text):
        """One vector per space-separated word of `text` (mean of its pieces' last hidden states)."""
        words = text.split()
        ids, owner = self.pieces(words)
        h = self.bert(input_ids=ids[None].to(self.old2new.device)).last_hidden_state[0]
        out = torch.zeros(len(words), self.dim, device=h.device, dtype=h.dtype)
        cnt = torch.zeros(len(words), 1, device=h.device, dtype=h.dtype)
        sel = owner >= 0
        out.index_add_(0, owner[sel].to(h.device), h[sel.to(h.device)])
        cnt.index_add_(0, owner[sel].to(h.device), torch.ones(int(sel.sum()), 1, device=h.device, dtype=h.dtype))
        return out / cnt.clamp(min=1), words
