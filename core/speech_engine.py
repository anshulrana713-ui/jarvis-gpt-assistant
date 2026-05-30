import win32com.client
import threading
from config import *

speaker = win32com.client.Dispatch("SAPI.SpVoice")
speak_lock = threading.Lock()

def shorten_for_speech(text, max_paragraphs=2, max_chars=MAX_SPEECH_CHARACTERS):
    text = str(text).strip()

    # Split by paragraph lines
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

    short_text = " ".join(paragraphs[:max_paragraphs])

    # Hard limit by characters
    if len(short_text) > max_chars:
        short_text = short_text[:max_chars].rsplit(" ", 1)[0] + "..."

    return short_text

def speak(text):
    def run():
        with speak_lock:
            try:
                spoken_text = shorten_for_speech(text)
                speaker.Speak(spoken_text)
            except Exception as e:
                print("Speech Error:", e)

    threading.Thread(target=run, daemon=True).start()

def auto_greet(add_chat):
    welcome_text = "Hello there! How can I help you today?"
    add_chat("jarvis GPT", welcome_text)
    speaker.Speak(welcome_text) 