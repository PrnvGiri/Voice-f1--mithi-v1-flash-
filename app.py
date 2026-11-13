"""Mithi v1 Flash - Web UI
Interactive Text-to-Speech playground for 11 Indian languages.
"""

import os
import sys
import time
import numpy as np
import gradio as gr

# Add current directory to path
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from mithi_tts import SR, Mithi

# Initialize model (cached globally)
print("Loading Mithi v1 Flash model...")
tts_model = Mithi(HERE)
print("Model loaded successfully!")

LANGUAGES = {
    "Hindi (hi)": "hi",
    "English (en)": "en",
    "Bengali (bn)": "bn",
    "Gujarati (gu)": "gu",
    "Kannada (kn)": "kn",
    "Malayalam (ml)": "ml",
    "Marathi (mr)": "mr",
    "Odia (or)": "or",
    "Punjabi (pa)": "pa",
    "Tamil (ta)": "ta",
    "Telugu (te)": "te",
}

VOICES = {
    "Charvi (Female)": "charvi",
    "Satvik (Male)": "satvik",
}

EXAMPLE_TEXTS = {
    "Hindi (hi)": "अरे, तुम आ गए! बहुत दिनों बाद मिले हो। चलो, पहले एक कप चाय पीते हैं, फिर आराम से बातें करेंगे।",
    "English (en)": "Wait, you actually got the tickets? That's amazing! I can't believe we're finally going to see them perform live.",
    "Bengali (bn)": "মা, আজ রাতে কী রান্না হচ্ছে? গন্ধটা তো দারুণ লাগছে! আমি কিন্তু খুব খিদে নিয়ে বাড়ি ফিরেছি।",
    "Gujarati (gu)": "કેમ છો? ઘણા દિવસે મળ્યા! ચાલો, આજે સાંજે સાથે ચા પીવા જઈએ.",
    "Kannada (kn)": "ನಮಸ್ಕಾರ! ನಿಮ್ಮ ಆರ್ಡರ್ ಈಗಾಗಲೇ ಹೊರಟಿದೆ, ನಾಳೆ ಮಧ್ಯಾಹ್ನದೊಳಗೆ ನಿಮ್ಮ ಮನೆಗೆ ತಲುಪುತ್ತದೆ.",
    "Malayalam (ml)": "ഹേയ്, എത്ര നാളായി കണ്ടിട്ട്! സുഖമാണോ? വാ, ഇന്ന് വൈകുന്നേരം നമുക്ക് ഒരുമിച്ച് ചായ കുടിക്കാം.",
    "Marathi (mr)": "आई, आज संध्याकाळी आपण सगळे मिळून बाहेर जेवायला जाऊया का? खूप दिवस झाले, सगळे एकत्र बसलो नाही.",
    "Odia (or)": "ଆରେ, କେତେ ଦିନ ପରେ ଦେଖା ହେଲା! କେମିତି ଅଛ? ଚାଲ, ଆଜି ସନ୍ଧ୍ୟାରେ ଏକାଠି ଚା ପିଇବା।",
    "Punjabi (pa)": "ਕੀ ਹਾਲ ਹੈ ਜੀ? ਬਹੁਤ ਦਿਨਾਂ ਬਾਅਦ ਮਿਲੇ ਹਾਂ! ਆਓ, ਅੱਜ ਸ਼ਾਮ ਨੂੰ ਇਕੱਠੇ ਚਾਹ ਪੀਂਦੇ ਹਾਂ।",
    "Tamil (ta)": "ஹேய், எவ்வளவு நாளாச்சு பார்த்து! எப்படி இருக்கீங்க? வாங்க, இன்னைக்கு சாயங்காலம் ஒன்னா காபி குடிக்கலாம்.",
    "Telugu (te)": "మీ టికెట్ కన్ಫರ್మ్ అయింది! రైలు రేపు ఉదయం ఆరు గంటలకు బయలుదేరుతుంది, కాబట్టి కొంచెం ముందుగానే స్టేషన్‌కి రండి.",
}


def synthesize(text, lang_label, voice_label, seed, gap):
    if not text or not text.strip():
        raise gr.Error("Please enter some text to synthesize.")

    lang = LANGUAGES.get(lang_label, "hi")
    voice = VOICES.get(voice_label, "charvi")
    seed_val = int(seed) if seed >= 0 else 0

    t0 = time.time()
    try:
        audio = tts_model.synthesize(
            text.strip(),
            lang=lang,
            voice=voice,
            seed=seed_val,
            gap=float(gap),
        )
    except Exception as e:
        raise gr.Error(f"Synthesis failed: {str(e)}")

    elapsed = time.time() - t0
    audio_dur = len(audio) / SR
    rtf = elapsed / audio_dur if audio_dur > 0 else 0

    status = (
        f"⚡ Generated **{audio_dur:.2f}s** of audio in **{elapsed:.2f}s** "
        f"({audio_dur / elapsed:.1f}x real-time, RTF: {rtf:.3f}) | **24 kHz Mono**"
    )

    return (SR, audio), status


def update_example_text(lang_label):
    return EXAMPLE_TEXTS.get(lang_label, "")


# Build UI
custom_css = """
.title-container { text-align: center; margin-bottom: 1.5rem; }
.badge { display: inline-block; padding: 2px 8px; border-radius: 9999px; font-size: 0.75rem; font-weight: 600; margin: 2px; }
.audio-output { margin-top: 10px; }
"""

with gr.Blocks(title="Mithi v1 Flash - TTS Playground") as demo:
    gr.HTML("""
    <div style="text-align: center; padding: 10px 0;">
        <h1 style="font-size: 2.2rem; font-weight: 700; margin-bottom: 0.25rem;">✨ Mithi v1 Flash</h1>
        <p style="font-size: 1.05rem; color: #64748b; margin-top: 0;">
            Fast, natural speech synthesis across 11 Indian languages with <b>Satvik</b> &amp; <b>Charvi</b> voices
        </p>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=5):
            with gr.Group():
                with gr.Row():
                    lang_dropdown = gr.Dropdown(
                        choices=list(LANGUAGES.keys()),
                        value="Hindi (hi)",
                        label="Select Language",
                        scale=3,
                    )
                    voice_radio = gr.Radio(
                        choices=list(VOICES.keys()),
                        value="Charvi (Female)",
                        label="Voice",
                        scale=2,
                    )

                text_input = gr.Textbox(
                    label="Input Text",
                    placeholder="Type or paste text in any of the 11 supported languages...",
                    value=EXAMPLE_TEXTS["Hindi (hi)"],
                    lines=4,
                    max_lines=12,
                )

                with gr.Accordion("⚙️ Advanced Settings", open=False):
                    with gr.Row():
                        seed_slider = gr.Slider(
                            minimum=0,
                            maximum=1000,
                            step=1,
                            value=0,
                            label="Random Seed",
                            info="Control prosody variations",
                        )
                        gap_slider = gr.Slider(
                            minimum=0.05,
                            maximum=0.5,
                            step=0.05,
                            value=0.15,
                            label="Sentence Pause Gap (seconds)",
                            info="Silence between sentences",
                        )

                with gr.Row():
                    btn_generate = gr.Button("🔊 Generate Audio", variant="primary", scale=3)
                    btn_clear = gr.Button("🗑️ Clear", variant="secondary", scale=1)

        with gr.Column(scale=4):
            audio_output = gr.Audio(
                label="Synthesized Audio (24 kHz)",
                type="numpy",
                autoplay=True,
            )
            status_markdown = gr.Markdown("Ready to synthesize.")

    # Update sample text automatically when language changes
    lang_dropdown.change(
        fn=update_example_text,
        inputs=[lang_dropdown],
        outputs=[text_input],
    )

    # Examples section
    gr.Markdown("### 💡 Quick Presets (Click any to test)")
    examples_data = [
        [EXAMPLE_TEXTS["Hindi (hi)"], "Hindi (hi)", "Charvi (Female)", 0, 0.15],
        [EXAMPLE_TEXTS["English (en)"], "English (en)", "Satvik (Male)", 0, 0.15],
        [EXAMPLE_TEXTS["Bengali (bn)"], "Bengali (bn)", "Charvi (Female)", 0, 0.15],
        [EXAMPLE_TEXTS["Gujarati (gu)"], "Gujarati (gu)", "Charvi (Female)", 0, 0.15],
        [EXAMPLE_TEXTS["Kannada (kn)"], "Kannada (kn)", "Charvi (Female)", 0, 0.15],
        [EXAMPLE_TEXTS["Malayalam (ml)"], "Malayalam (ml)", "Charvi (Female)", 0, 0.15],
        [EXAMPLE_TEXTS["Marathi (mr)"], "Marathi (mr)", "Charvi (Female)", 0, 0.15],
        [EXAMPLE_TEXTS["Odia (or)"], "Odia (or)", "Charvi (Female)", 0, 0.15],
        [EXAMPLE_TEXTS["Punjabi (pa)"], "Punjabi (pa)", "Charvi (Female)", 0, 0.15],
        [EXAMPLE_TEXTS["Tamil (ta)"], "Tamil (ta)", "Charvi (Female)", 0, 0.15],
        [EXAMPLE_TEXTS["Telugu (te)"], "Telugu (te)", "Charvi (Female)", 0, 0.15],
    ]

    gr.Examples(
        examples=examples_data,
        inputs=[text_input, lang_dropdown, voice_radio, seed_slider, gap_slider],
        outputs=[audio_output, status_markdown],
        fn=synthesize,
        cache_examples=False,
    )

    # Event handlers
    btn_generate.click(
        fn=synthesize,
        inputs=[text_input, lang_dropdown, voice_radio, seed_slider, gap_slider],
        outputs=[audio_output, status_markdown],
    )

    btn_clear.click(
        fn=lambda: ("", None, "Ready."),
        inputs=[],
        outputs=[text_input, audio_output, status_markdown],
    )

if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True,
        inbrowser=True,
    )
