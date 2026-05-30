import speech_recognition as sr
import threading

recognizer = sr.Recognizer()

def get_voice_input(root, add_chat, entry, get_response, speak):
    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)

            root.after(0, lambda: add_chat("jarvis GPT", "Listening..."))

            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=6
            )

        text = recognizer.recognize_google(audio)

        root.after(0, lambda: add_chat("You", text))
        root.after(0, lambda: entry.delete(0, "end"))
        root.after(0, lambda: entry.insert(0, text))
        root.after(0, get_response)

    except sr.UnknownValueError:
        root.after(0, lambda: add_chat("jarvis GPT", "Sorry, I didn't understand that."))
        speak("Sorry, I didn't understand that.")

    except sr.WaitTimeoutError:
        root.after(0, lambda: add_chat("jarvis GPT", "No speech detected."))
        speak("No speech detected.")

    except Exception:
        root.after(0, lambda: add_chat("jarvis GPT", "Microphone error."))
        speak("Microphone error.")

def wake_word_listener(root, add_chat, speak, start_voice_input):
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)

                print("Listening for Jarvis...")

                audio = recognizer.listen(source,timeout=None,phrase_time_limit=3)

            text = recognizer.recognize_google(audio).lower().strip()

            print("Heard:", text)

            if text == "jarvis":
                root.after(0, lambda: add_chat("jarvis GPT", "Yes boss?"))
                speak("Yes boss")

                root.after(1500,lambda: threading.Thread(target=start_voice_input,daemon=True).start())
        except:
            pass

def start_wake_listener(
    root,
    add_chat,
    entry,
    get_response,
    speak
):
    threading.Thread(
        target=wake_word_listener,
        args=(root, add_chat, speak,
              lambda: get_voice_input(
                  root,
                  add_chat,
                  entry,
                  get_response,
                  speak
              )),
        daemon=True
    ).start()        