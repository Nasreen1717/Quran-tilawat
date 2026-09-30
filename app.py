import asyncio
import os

import edge_tts
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# Pehle jo model available ho wo use hoga (Groq ki list se automatically)
PREFERRED_MODELS = [
    "openai/gpt-oss-120b",
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-20b",
    "qwen/qwen3-32b",
    "llama-3.1-8b-instant",
]
SKIP_WORDS = ("whisper", "guard", "tts", "safeguard", "compound", "orpheus")

# Option 1 (default): Urdu voice, poora text ek hi bar mein, ek hi flow mein
VOICES = {
    "Asad (Urdu, mard, news ke liye best)": "ur-PK-AsadNeural",
    "Uzma (Urdu, aurat)": "ur-PK-UzmaNeural",
}

# Option 2 (test ke liye): Multilingual voices, ek hi voice mein Urdu + English.
# Urdu officially supported nahi, is liye pehle sun kar check karein.
MULTI_VOICES = {
    "Andrew Multilingual (test)": "en-US-AndrewMultilingualNeural",
    "Brian Multilingual (test)": "en-US-BrianMultilingualNeural",
    "Ava Multilingual (test)": "en-US-AvaMultilingualNeural",
    "Emma Multilingual (test)": "en-US-EmmaMultilingualNeural",
}

ALL_VOICES = {**VOICES, **MULTI_VOICES}

SYSTEM_PROMPT = """You are an Urdu news script editor for a text-to-speech system.

Task: Convert the user's text into clean Urdu script (Arabic script, Nastaliq style spelling) ready to be read aloud by a news caster in one smooth, continuous flow.

Rules:
1. If the input is Roman Urdu, convert it to correct Urdu script. If it is already Urdu script, only clean it.
2. Write all numbers, dates, years, times, currencies and percentages as Urdu words (for example: 2024 becomes دو ہزار چوبیس, 15% becomes پندرہ فیصد).
3. Expand abbreviations so they are read correctly.
4. Punctuation controls pauses, so use it sparingly. Put ۔ only at the real end of a sentence. Put ، only where a real news caster would naturally pause for meaning (between clauses, after an introductory phrase, between items in a list). Never put a comma or full stop right before or after an English word or term just because it is English. Do not chop a sentence into small pieces. Keep the natural flow of a news bulletin.
5. Keep ALL English words, English terms, brand names and acronyms in English (Latin) letters exactly as they are, written inline inside the Urdu sentence without any extra punctuation around them. Do NOT transliterate them into Urdu script. Example: 'AI ٹیکنالوجی' and 'Google نے نیا feature متعارف کرایا' stay with AI, Google and feature in English. Only Urdu and Roman Urdu words become Urdu script. Numbers that are part of an English term (like iPhone 15 or GPT-4) stay as they are.
6. Do NOT add, remove or change facts. Do NOT add opinions or extra sentences.
7. Keep paragraph breaks (blank lines) as they are.
8. Output ONLY the final Urdu text. No explanations, no quotes, no markdown."""


def get_api_key():
    key = os.getenv("GROQ_API_KEY")
    if key:
        return key
    try:
        return st.secrets["GROQ_API_KEY"]
    except Exception:
        return None


@st.cache_data(ttl=3600, show_spinner=False)
def get_models(api_key: str):
    """Groq se current models ki list lata hai."""
    try:
        client = OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)
        ids = [m.id for m in client.models.list().data]
        ids = [i for i in ids if not any(w in i.lower() for w in SKIP_WORDS)]
        ordered = [m for m in PREFERRED_MODELS if m in ids]
        rest = sorted(i for i in ids if i not in ordered)
        return ordered + rest or PREFERRED_MODELS
    except Exception:
        return PREFERRED_MODELS


def prepare_text(text: str, api_key: str, model: str) -> str:
    client = OpenAI(api_key=api_key, base_url=GROQ_BASE_URL)
    response = client.chat.completions.create(
        model=model,
        temperature=0.1,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content.strip()


async def _speak(text: str, voice: str, rate: int, pitch: int, volume: int) -> bytes:
    communicate = edge_tts.Communicate(
        text,
        voice,
        rate=f"{rate:+d}%",
        pitch=f"{pitch:+d}Hz",
        volume=f"{volume:+d}%",
    )
    audio = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio += chunk["data"]
    return audio


def synthesize(text: str, voice: str, rate: int, pitch: int, volume: int) -> bytes:
    # Poora text ek hi voice se ek hi bar mein synthesize hota hai,
    # is liye awaaz tor tor ke nahi aati aur flow news caster jaisa rehta hai.
    # Engine swap ke liye sirf ye function badalna hai (Azure, ElevenLabs, etc.)
    return asyncio.run(_speak(text, voice, rate, pitch, volume))


st.set_page_config(page_title="Urdu Voice Agent", page_icon="🎙️")
st.title("🎙️ Urdu News Voice Agent")
st.caption("Roman Urdu ya Urdu script likhein, news-caster style awaaz milegi.")

api_key = get_api_key()

with st.sidebar:
    st.header("Voice settings")
    voice_label = st.selectbox("Voice", list(ALL_VOICES.keys()))
    if voice_label in MULTI_VOICES:
        st.info("Multilingual voice test mode hai. Urdu ka talaffuz sun kar check karein; theek na lage to Asad par wapas jayein.")
    rate = st.slider("Speed (%)", -30, 30, -5)
    pitch = st.slider("Pitch (Hz)", -30, 30, -4)
    volume = st.slider("Volume (%)", -30, 30, 0)
    use_groq = st.checkbox("Groq cleanup (Roman to Urdu, numbers, pauses)", value=True)
    model = None
    if use_groq:
        if api_key:
            model = st.selectbox("Groq model", get_models(api_key))
        else:
            st.error("GROQ_API_KEY missing hai. .env check karein.")

text_input = st.text_area(
    "Script",
    height=220,
    placeholder="Yahan Roman Urdu ya Urdu script likhein...",
)

if st.button("Generate voice", type="primary"):
    if not text_input.strip():
        st.warning("Pehle script likhein.")
        st.stop()

    final_text = text_input.strip()

    if use_groq:
        if not api_key or not model:
            st.error("GROQ_API_KEY missing hai. .env file check karein.")
            st.stop()
        with st.spinner("Groq text tayyar kar raha hai..."):
            try:
                final_text = prepare_text(final_text, api_key, model)
            except Exception as e:
                st.error(f"Groq error: {e}")
                st.stop()

    with st.spinner("Awaaz ban rahi hai..."):
        try:
            audio_bytes = synthesize(final_text, ALL_VOICES[voice_label], rate, pitch, volume)
        except Exception as e:
            st.error(f"Edge TTS error: {e}")
            st.stop()

    if not audio_bytes:
        st.error("Audio nahi bani. Internet check karein ya dusri voice try karein.")
        st.stop()

    # Result session_state mein save hota hai, taake download dabane par gayab na ho
    st.session_state["final_text"] = final_text
    st.session_state["audio"] = audio_bytes

if "audio" in st.session_state:
    st.subheader("Result")
    with st.expander("Converted text", expanded=True):
        st.markdown(
            f"<div dir='rtl' style='font-size:22px; line-height:2;'>{st.session_state['final_text']}</div>",
            unsafe_allow_html=True,
        )
    st.audio(st.session_state["audio"], format="audio/mp3")
    st.download_button(
        "⬇️ Download MP3",
        st.session_state["audio"],
        file_name="voiceover.mp3",
        mime="audio/mpeg",
    )
