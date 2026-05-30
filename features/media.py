import webbrowser
import pywhatkit

def open_youtube():
    webbrowser.open("https://www.youtube.com")
    return "Opening YouTube"

def open_google():
    webbrowser.open("https://www.google.com")
    return "Opening Google"

def open_whatsapp():
    webbrowser.open("https://web.whatsapp.com")
    return "Opening WhatsApp"

def play_song(song):
    if song.strip() == "":
        return "What do you want me to play?"

    pywhatkit.playonyt(song)
    return f"Playing {song} on YouTube"