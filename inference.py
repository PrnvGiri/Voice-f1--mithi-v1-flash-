"""Mithi v1 Flash: text -> speech.

    python inference.py --lang hi --text "आज मौसम कितना अच्छा है!" --voice charvi --out hello.wav
    python inference.py --lang en --text "Hello! How are you today?" --voice satvik --out hello_en.wav
    python inference.py --device cpu --threads 4 --lang hi --text "नमस्ते! आप कैसे हैं?" --out hello_cpu.wav

Languages: hi en bn gu kn ml mr or pa ta te    Voices: satvik (male), charvi (female)
"""
import argparse
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mithi_tts import SR, Mithi  # noqa: E402

ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
ap.add_argument("--text", required=True, help="text to speak")
ap.add_argument("--lang", default="hi", help="hi en bn gu kn ml mr or pa ta te")
ap.add_argument("--voice", default="charvi", help="satvik or charvi")
ap.add_argument("--out", default="output.wav", help="output .wav file")
ap.add_argument("--device", default=None, help="cuda or cpu (default: cuda if available)")
ap.add_argument("--threads", type=int, default=None, help="CPU threads (default: PyTorch's choice, usually all cores)")
args = ap.parse_args()

if args.threads:
    import torch
    torch.set_num_threads(args.threads)

tts = Mithi(HERE, device=args.device)
t0 = time.time()
audio = tts.synthesize(args.text, lang=args.lang, voice=args.voice)
tts.save(audio, args.out)
print(f"{args.out}: {len(audio) / SR:.2f} s of audio in {time.time() - t0:.2f} s")
