---
license: apache-2.0
language:
  - hi
  - en
  - bn
  - gu
  - kn
  - ml
  - mr
  - or
  - pa
  - ta
  - te
pipeline_tag: text-to-speech
tags:
  - text-to-speech
  - tts
  - indic
  - kokoro
  - bf16
---

# Mithi v1 Flash

A small text-to-speech model for 11 Indian languages, with two voices: **Satvik** (male) and **Charvi** (female).

- **Languages:** Hindi, English, Bengali, Gujarati, Kannada, Malayalam, Marathi, Odia, Punjabi, Tamil, Telugu.
- **Size:** 99.1 M parameters, 197 MB.
- **Weights:** bf16 safetensors. Load them into fp32 and compute in fp32.
- **Output:** 24 kHz mono audio.

## Voices

One male and one female speaker. Their training speech was generated with Maya2-native inference.

| Voice | Speaker |
|---|---|
| **Satvik** | Male |
| **Charvi** | Female |

## Model

```
text
 └─ text normaliser               numbers, dates, currency, URLs ... → words
 └─ espeak-ng / misaki G2P        → phonemes (Kokoro's phoneme set)
 └─ indic-bert                    one meaning vector per word
 └─ prosody writer                per phoneme: duration, voicing, 5 pitch points, 3 loudness points, breath
 └─ Kokoro text encoder + iSTFTNet decoder → 24 kHz audio
```

| Component | Parameters | Files |
|---|---|---|
| indic-bert (ALBERT, word table trimmed to 105,229 pieces) | 21.3 M | `indic_encoder/` |
| Prosody writer (Transformer reader + autoregressive writer) | 18.8 M | `writer.safetensors` |
| Kokoro text encoder + iSTFTNet decoder (fine-tuned) | 58.9 M | `decoder.safetensors`, `kokoro_config.json` |
| Voice style vectors, Satvik and Charvi (510 × 1 × 256 each) | n/a | `voices.safetensors` |

**Prosody writer.** It writes the prosody one phoneme at a time, as codes:
- one code for the duration, in 25 ms units;
- one code for whether the phoneme is voiced, plus the unvoiced frames at its start and end;
- five pitch points, in 0.5-semitone steps relative to 100 Hz;
- three loudness points;
- one code that says whether to insert a breath.

Each token's codes are predicted in order, each seeing the ones before it. The codes become frame-level pitch and energy curves, two frames per 25 ms. The Kokoro decoder turns them into audio, styled by the voice vector of the chosen speaker.

## Inference settings

These are in `config.json`, field `inference`:

| Setting | Value |
|---|---|
| Writer temperature, top-p | 0.7, 1.0 |
| Voicing codes | greedy (temperature 0) |
| Silence at each end | at most 2 units (50 ms) |
| Pitch shift | +0.6 semitone |
| Random seed | 0 for every sentence (same text, same audio) |
| Long text | read in pieces of at most 400 phonemes (sentences, then comma pieces), joined with 0.15 s of silence |

The writer's language order is `hi en bn gu kn ml mr or pa ta te as`; it is stored in the metadata of `writer.safetensors`. Its voice order is `satvik charvi`.

## Precision

Compute in fp32. Running the iSTFTNet decoder with bf16 arithmetic adds audible noise inside the voice. On identical prosody it changes the output by a log-mel distance of 0.196, against 0.037 for bf16 weights with fp32 arithmetic.

## Files

| File | Contents |
|---|---|
| `config.json` | languages, voices, components, inference settings |
| `decoder.safetensors` | Kokoro text encoder (`text_encoder.*`) and iSTFTNet decoder (`decoder.*`) |
| `kokoro_config.json` | decoder dimensions and the phoneme vocabulary |
| `writer.safetensors` | prosody writer; its metadata holds the voice and language order |
| `voices.safetensors` | `satvik`, `charvi` style vectors (row = phoneme count − 1) |
| `indic_encoder/` | indic-bert weights and config, SentencePiece model, `old2new.npy` (SentencePiece id → trimmed table id) |

## Limitations

**Voice and style**
- **Less expressive than Maya2-native.** Intonation and emotion are flatter than in the speech it learned from.
- **Two voices only.** Satvik and Charvi; there is no voice cloning.
- **Pitch correction at inference.** The +0.6 semitone pitch shift corrects a slightly low pitch from the writer. The model did not learn it.

**Languages**
- **Kannada, Malayalam, Marathi, Odia:** speech can come out a little faster than natural.
- **Odia:** ୱ should be written as ବ before phonemising, because espeak-ng spells words containing ୱ letter by letter.
- **English words inside Indian-language text:** they are pronounced with the English G2P, in the same voice.
- **Assamese:** not supported, although the writer has an Assamese language slot.
- **Pronunciation:** it depends on espeak-ng / misaki. A word the G2P gets wrong is spoken wrong.
- **Numbers, dates, currency, URLs:** they are read only as well as the text normaliser expands them.

**Long text**
- **Read in pieces.** Text over 400 phonemes is read in pieces (sentences, then comma pieces) joined with 0.15 s of silence. Each piece's prosody is written without seeing the others.
- **Phoneme limit.** One piece can be at most 510 phonemes, the length of the voice tables.
- **Word mismatch.** If a sentence's words and phoneme groups do not line up, the writer reads that sentence from phonemes alone, without the indic-bert meaning vectors. This is rare.

**Precision and runtime**
- **fp32 arithmetic only.** bf16 arithmetic in the iSTFTNet decoder adds audible noise. Only the stored weights are bf16.
- **G2P dependency.** It needs espeak-ng (GPL-3.0, through phonemizer), which matters when bundling it into closed-source apps.
- **Autoregressive writer.** It writes one phoneme at a time, so compute grows with sentence length.

**Evaluation**
- **No published evaluation.** This card reports no automated scores (ASR error rate, speaker similarity) and no human listening study (MOS).

## Credits and licences

- **Kokoro-82M** text encoder and iSTFTNet decoder: [hexgrad/kokoro](https://github.com/hexgrad/kokoro), Apache-2.0.
- **indic-bert:** [ai4bharat/indic-bert](https://huggingface.co/ai4bharat/indic-bert), MIT.
- **G2P:** [misaki](https://github.com/hexgrad/misaki) and espeak-ng.
- **Training audio:** the prosody writer and decoder were trained on speech generated with Maya2-native for the Satvik and Charvi voices.
