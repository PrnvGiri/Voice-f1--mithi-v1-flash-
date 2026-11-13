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
  - bf16
---

<p align="center">
  <img src="https://huggingface.co/Oomni/mithi-v1-flash/resolve/main/assets/mithi_banner.png" alt="Mithi: sweet, natural speech in 11 Indian languages" width="100%">
</p>

# Voice-F1: Mithi v1 Flash Text-to-Speech

A fast, lightweight, and natural text-to-speech (TTS) system for **11 Indian languages** powered by **Mithi v1 Flash**, complete with an interactive Web UI and Python/CLI inference support.

---

## Features

- 🌐 **11 Supported Languages**: Hindi (`hi`), English (`en`), Bengali (`bn`), Gujarati (`gu`), Kannada (`kn`), Malayalam (`ml`), Marathi (`mr`), Odia (`or`), Punjabi (`pa`), Tamil (`ta`), and Telugu (`te`).
- 🎙️ **2 Expressive Voices**:
  - **Charvi** (Female)
  - **Satvik** (Male)
- ⚡ **Blazing Fast**: Faster than real-time on Apple Silicon and modern CPUs; GPU acceleration via CUDA supported.
- 🔊 **Studio Quality**: 24 kHz mono WAV output.
- 🖥️ **Interactive Web UI**: Powered by Gradio with live waveform playback, instant 1-click sample presets for every language, audio download, and prosody controls.

---

## Requirements & Prerequisites

> [!IMPORTANT]
> **Python Version Requirement**: `misaki` requires **Python >= 3.8 and < 3.13** (e.g., **Python 3.10, 3.11, or 3.12**).
> Do **not** use Python 3.13+ or 3.14.

---

## Quickstart

### 1. Set Up Virtual Environment

```bash
# Clone or navigate to the repository
cd voice-f1/mithi-v1-flash

# Create virtual environment using Python 3.11
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## How to Use

### Option 1: Launch the Interactive Web UI (Recommended)

To start the local web interface:

```bash
python app.py
```

Once started, open your browser and navigate to:
👉 **[http://127.0.0.1:7860](http://127.0.0.1:7860)**

#### Web UI Controls:
- **Select Language**: Pick any of the 11 languages from the dropdown. The input text automatically populates with a native conversational sample.
- **Select Voice**: Toggle between **Charvi (Female)** and **Satvik (Male)**.
- **Input Text**: Type or paste text in any supported script or English.
- **Advanced Settings**:
  - **Random Seed**: Adjust to experiment with subtle phrasing and prosody nuances.
  - **Sentence Pause Gap**: Set the duration of silence between sentences (default `0.15s`).
- **Quick Presets Table**: Click any row in the examples table to instantly load and test different languages.
- **Audio Output**: Listen to generated speech directly in your browser or download the `.wav` file.

---

### Option 2: Command-Line (CLI) Inference

You can synthesize speech directly from your terminal using `inference.py`:

```bash
# Hindi with Charvi (female voice)
python inference.py --lang hi --voice charvi --text "आज मौसम कितना अच्छा है! चलो, शाम को कहीं बाहर घूमने चलते हैं।" --out hindi.wav

# English with Satvik (male voice)
python inference.py --lang en --voice satvik --text "Your appointment is confirmed for Monday at 10:30 AM." --out english.wav

# Bengali
python inference.py --lang bn --voice charvi --text "মা, আজ রাতে কী রান্না হচ্ছে? আমি কিন্তু খুব খিদে নিয়ে বাড়ি ফিরেছি।" --out bengali.wav

# Specify CPU thread count
python inference.py --device cpu --threads 4 --lang hi --voice charvi --text "नमस्ते! आप कैसे हैं?" --out hello_cpu.wav
```

#### CLI Options:
| Flag | Description | Default |
|---|---|---|
| `--text` | Text to synthesize *(required)* | - |
| `--lang` | Language code (`hi`, `en`, `bn`, `gu`, `kn`, `ml`, `mr`, `or`, `pa`, `ta`, `te`) | `hi` |
| `--voice` | Voice name (`charvi` or `satvik`) | `charvi` |
| `--out` | Output file path (`.wav`) | `output.wav` |
| `--device` | Device to run on (`cpu`, `cuda`) | Auto-detect |
| `--threads` | Number of CPU threads | PyTorch default |

---

### Option 3: Python API

You can integrate Mithi into your own Python applications:

```python
from mithi_tts import Mithi, SR

# Load model (loads weights once)
tts = Mithi(".")

# Synthesize speech (returns float32 numpy array at 24 kHz)
audio = tts.synthesize(
    text="नमस्ते! आप कैसे हैं?",
    lang="hi",
    voice="satvik",
    gap=0.15
)

# Save to 24 kHz WAV
tts.save(audio, "output_hindi.wav")
```

---

## Supported Languages Reference

| Language | Code | Native Name | Sample Script |
|---|---|---|---|
| **Hindi** | `hi` | हिन्दी | आज मौसम कितना अच्छा है! |
| **English** | `en` | English | Hello! How are you today? |
| **Bengali** | `bn` | বাংলা | নমস্কার! আপনি কেমন আছেন? |
| **Gujarati** | `gu` | ગુજરાતી | કેમ છો? આજે કેવો દિવસ રહ્યો? |
| **Kannada** | `kn` | ಕನ್ನಡ | ನಮಸ್ಕಾರ! ನೀವು ಹೇಗಿದ್ದೀರಿ? |
| **Malayalam** | `ml` | മലയാളം | നമസ്കാരം! സുഖമാണോ? |
| **Marathi** | `mr` | मराठी | नमस्कार! तुम्ही कसे आहात? |
| **Odia** | `or` | ଓଡ଼ିଆ | ନମସ୍କାର! ଆପଣ କେମିତି ଅଛନ୍ତି? |
| **Punjabi** | `pa` | ਪੰਜਾਬੀ | ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ! ਤੁਹਾਡਾ ਕੀ ਹਾਲ ਹੈ? |
| **Tamil** | `ta` | தமிழ் | வணக்கம்! நீங்கள் எப்படி இருக்கிறீர்கள்? |
| **Telugu** | `te` | తెలుగు | నమస్కారం! మీరు ఎలా ఉన్నారు? |

---

## License

Mithi v1 Flash model weights and inference code are released under the **Apache-2.0 License**.
