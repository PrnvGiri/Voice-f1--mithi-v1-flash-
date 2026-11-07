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

## Samples

Every sentence in both voices: 11 languages, one conversational line and one news or education line with numbers.
The text is shown as typed; numbers, times and currency are expanded into words by the text normaliser.

### Conversational

| Sentence | Satvik (male) | Charvi (female) |
|---|:---:|:---:|
| **Hindi**<br>अरे, तुम आ गए! बहुत दिनों बाद मिले हो। चलो, पहले एक कप चाय पीते हैं, फिर आराम से बातें करेंगे। | <audio controls preload="none" aria-label="Hindi, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/hi_conversational_satvik.wav"></audio> | <audio controls preload="none" aria-label="Hindi, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/hi_conversational_charvi.wav"></audio> |
| **English**<br>Wait, you actually got the tickets? That's amazing! I can't believe we're finally going to see them live. | <audio controls preload="none" aria-label="English, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/en_conversational_satvik.wav"></audio> | <audio controls preload="none" aria-label="English, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/en_conversational_charvi.wav"></audio> |
| **Bengali**<br>মা, আজ রাতে কী রান্না হচ্ছে? গন্ধটা তো দারুণ লাগছে! আমি কিন্তু খুব খিদে নিয়ে বাড়ি ফিরেছি। | <audio controls preload="none" aria-label="Bengali, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/bn_conversational_satvik.wav"></audio> | <audio controls preload="none" aria-label="Bengali, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/bn_conversational_charvi.wav"></audio> |
| **Gujarati**<br>કેમ છો? ઘણા દિવસે મળ્યા! ચાલો, આજે સાંજે સાથે ચા પીવા જઈએ. | <audio controls preload="none" aria-label="Gujarati, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/gu_conversational_satvik.wav"></audio> | <audio controls preload="none" aria-label="Gujarati, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/gu_conversational_charvi.wav"></audio> |
| **Kannada**<br>ನಮಸ್ಕಾರ! ನಿಮ್ಮ ಆರ್ಡರ್ ಈಗಾಗಲೇ ಹೊರಟಿದೆ, ನಾಳೆ ಮಧ್ಯಾಹ್ನದೊಳಗೆ ನಿಮ್ಮ ಮನೆಗೆ ತಲುಪುತ್ತದೆ. ಇನ್ನೇನಾದರೂ ಸಹಾಯ ಬೇಕಾ? | <audio controls preload="none" aria-label="Kannada, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/kn_conversational_satvik.wav"></audio> | <audio controls preload="none" aria-label="Kannada, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/kn_conversational_charvi.wav"></audio> |
| **Malayalam**<br>ഹേയ്, എത്ര നാളായി കണ്ടിട്ട്! സുഖമാണോ? വാ, ഇന്ന് വൈകുന്നേരം നമുക്ക് ഒരുമിച്ച് ചായ കുടിക്കാം. | <audio controls preload="none" aria-label="Malayalam, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/ml_conversational_satvik.wav"></audio> | <audio controls preload="none" aria-label="Malayalam, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/ml_conversational_charvi.wav"></audio> |
| **Marathi**<br>आई, आज संध्याकाळी आपण सगळे मिळून बाहेर जेवायला जाऊया का? खूप दिवस झाले, सगळे एकत्र बसलो नाही. | <audio controls preload="none" aria-label="Marathi, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/mr_conversational_satvik.wav"></audio> | <audio controls preload="none" aria-label="Marathi, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/mr_conversational_charvi.wav"></audio> |
| **Odia**<br>ଆରେ, କେତେ ଦିନ ପରେ ଦେଖା ହେଲା! କେମିତି ଅଛ? ଚାଲ, ଆଜି ସନ୍ଧ୍ୟାରେ ଏକାଠି ଚା ପିଇବା। | <audio controls preload="none" aria-label="Odia, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/or_conversational_satvik.wav"></audio> | <audio controls preload="none" aria-label="Odia, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/or_conversational_charvi.wav"></audio> |
| **Punjabi**<br>ਕੀ ਹਾਲ ਹੈ ਜੀ? ਬਹੁਤ ਦਿਨਾਂ ਬਾਅਦ ਮਿਲੇ ਹਾਂ! ਆਓ, ਅੱਜ ਸ਼ਾਮ ਨੂੰ ਇਕੱਠੇ ਚਾਹ ਪੀਂਦੇ ਹਾਂ। | <audio controls preload="none" aria-label="Punjabi, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/pa_conversational_satvik.wav"></audio> | <audio controls preload="none" aria-label="Punjabi, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/pa_conversational_charvi.wav"></audio> |
| **Tamil**<br>ஹேய், எவ்வளவு நாளாச்சு பார்த்து! எப்படி இருக்கீங்க? வாங்க, இன்னைக்கு சாயங்காலம் ஒன்னா காபி குடிக்கலாம். | <audio controls preload="none" aria-label="Tamil, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/ta_conversational_satvik.wav"></audio> | <audio controls preload="none" aria-label="Tamil, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/ta_conversational_charvi.wav"></audio> |
| **Telugu**<br>మీ టికెట్ కన్ఫర్మ్ అయింది! రైలు రేపు ఉదయం ఆరు గంటలకు బయలుదేరుతుంది, కాబట్టి కొంచెం ముందుగానే స్టేషన్‌కి రండి. | <audio controls preload="none" aria-label="Telugu, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/te_conversational_satvik.wav"></audio> | <audio controls preload="none" aria-label="Telugu, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/te_conversational_charvi.wav"></audio> |

### News and education, with numbers

| Sentence | Satvik (male) | Charvi (female) |
|---|:---:|:---:|
| **Hindi**<br>भारतीय अंतरिक्ष अनुसंधान संगठन ने आज सुबह 9:30 बजे श्रीहरिकोटा से एक नया उपग्रह सफलतापूर्वक लॉन्च किया, जिसकी लागत लगभग ₹450 करोड़ है। | <audio controls preload="none" aria-label="Hindi, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/hi_news_satvik.wav"></audio> | <audio controls preload="none" aria-label="Hindi, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/hi_news_charvi.wav"></audio> |
| **English** · Education<br>Light from the Sun takes about 8 minutes and 20 seconds to reach the Earth, travelling nearly 150 million kilometres. | <audio controls preload="none" aria-label="English, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/en_education_satvik.wav"></audio> | <audio controls preload="none" aria-label="English, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/en_education_charvi.wav"></audio> |
| **Bengali**<br>রাজ্যের মাধ্যমিক পরীক্ষায় এ বছর 92 শতাংশ ছাত্রছাত্রী পাশ করেছে, যা গত বছরের চেয়ে 3 শতাংশ বেশি। | <audio controls preload="none" aria-label="Bengali, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/bn_news_satvik.wav"></audio> | <audio controls preload="none" aria-label="Bengali, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/bn_news_charvi.wav"></audio> |
| **Gujarati**<br>ગુજરાતમાં આ વર્ષે 1,250 નવી શાળાઓ શરૂ કરવામાં આવશે, જેનાથી આશરે 2 લાખ બાળકોને લાભ મળશે. | <audio controls preload="none" aria-label="Gujarati, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/gu_news_satvik.wav"></audio> | <audio controls preload="none" aria-label="Gujarati, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/gu_news_charvi.wav"></audio> |
| **Kannada**<br>ಬೆಂಗಳೂರಿನ ಮೆಟ್ರೋದಲ್ಲಿ ಕಳೆದ ತಿಂಗಳು ಪ್ರತಿದಿನ ಸರಾಸರಿ 8 ಲಕ್ಷ ಜನರು ಪ್ರಯಾಣಿಸಿದ್ದಾರೆ ಎಂದು ಅಧಿಕಾರಿಗಳು ತಿಳಿಸಿದ್ದಾರೆ. | <audio controls preload="none" aria-label="Kannada, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/kn_news_satvik.wav"></audio> | <audio controls preload="none" aria-label="Kannada, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/kn_news_charvi.wav"></audio> |
| **Malayalam**<br>കേരളത്തിലെ ഡിജിറ്റൽ സാക്ഷരതാ പദ്ധതിയിലൂടെ 65 വയസ്സിന് മുകളിലുള്ള 2 ലക്ഷത്തിലധികം പേർ സ്മാർട്ട്ഫോൺ ഉപയോഗിക്കാൻ പഠിച്ചു. | <audio controls preload="none" aria-label="Malayalam, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/ml_news_satvik.wav"></audio> | <audio controls preload="none" aria-label="Malayalam, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/ml_news_charvi.wav"></audio> |
| **Marathi**<br>पुण्यात आज सकाळी 7 वाजता 12 अंश सेल्सिअस तापमानाची नोंद झाली, जे या हिवाळ्यातील सर्वात कमी तापमान आहे. | <audio controls preload="none" aria-label="Marathi, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/mr_news_satvik.wav"></audio> | <audio controls preload="none" aria-label="Marathi, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/mr_news_charvi.wav"></audio> |
| **Odia**<br>ଓଡ଼ିଶାରେ ଏହି ବର୍ଷ 3,500 ନୂଆ ଶିକ୍ଷକ ନିଯୁକ୍ତ ହେବେ ବୋଲି ସରକାର ଆଜି ଘୋଷଣା କରିଛନ୍ତି। | <audio controls preload="none" aria-label="Odia, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/or_news_satvik.wav"></audio> | <audio controls preload="none" aria-label="Odia, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/or_news_charvi.wav"></audio> |
| **Punjabi**<br>ਪੰਜਾਬ ਵਿੱਚ ਇਸ ਸਾਲ ਕਣਕ ਦੀ ਪੈਦਾਵਾਰ 180 ਲੱਖ ਟਨ ਤੱਕ ਪਹੁੰਚ ਗਈ ਹੈ, ਜੋ ਪਿਛਲੇ ਸਾਲ ਨਾਲੋਂ 5 ਫ਼ੀਸਦੀ ਵੱਧ ਹੈ। | <audio controls preload="none" aria-label="Punjabi, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/pa_news_satvik.wav"></audio> | <audio controls preload="none" aria-label="Punjabi, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/pa_news_charvi.wav"></audio> |
| **Tamil**<br>சென்னையில் நேற்று 45 மில்லிமீட்டர் மழை பதிவானது, மேலும் அடுத்த 2 நாட்களுக்கு மழை தொடரும் என்று வானிலை ஆய்வு மையம் தெரிவித்துள்ளது. | <audio controls preload="none" aria-label="Tamil, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/ta_news_satvik.wav"></audio> | <audio controls preload="none" aria-label="Tamil, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/ta_news_charvi.wav"></audio> |
| **Telugu**<br>హైదరాబాద్‌లో ఈ ఏడాది 2,000 కొత్త ఎలక్ట్రిక్ బస్సులు ప్రవేశపెట్టనున్నట్లు ప్రభుత్వం ప్రకటించింది. | <audio controls preload="none" aria-label="Telugu, Satvik" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/te_news_satvik.wav"></audio> | <audio controls preload="none" aria-label="Telugu, Charvi" src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/samples/te_news_charvi.wav"></audio> |

All clips and their text (`samples/sentences.tsv`) are in the [`samples/`](https://huggingface.co/Oomni/mithi-v1-flash/tree/main/samples) folder.

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
| `samples/` | 44 example clips (11 languages × 2 sentences × 2 voices) and `sentences.tsv` |
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
