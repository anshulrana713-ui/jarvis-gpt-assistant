import google.generativeai as ai
import win32com.client
import speech_recognition as sr
import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
import threading
import datetime
import webbrowser
import os
import pyautogui
import platform
import screen_brightness_control as sbc
import pyaudio
import pywhatkit
import requests
import feedparser
import json
from tkinter import filedialog
stop_speaking = False
engine = None
speaker = win32com.client.Dispatch("SAPI.SpVoice")

ai.configure(api_key="AIzaSyDsYkpBk9yJNjgCa5GNGhD-3TVyoim_wno")
model = ai.GenerativeModel(model_name="gemini-3-flash-preview")
chat = model.start_chat()


recognizer = sr.Recognizer()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title("jarvis GPT")
root.geometry("980x650+350+20")

title_label = ctk.CTkLabel(root, text="jarvis GPT", font=("Comic Sans MS", 35, "bold"))
title_label.place(relx=0.5, rely=0.04, anchor="center")

gif_path = "terminator.gif"
gif = Image.open(gif_path)
frames = [ImageTk.PhotoImage(frame.convert("RGBA")) for frame in ImageSequence.Iterator(gif)]

frame_index = 0

canvas = ctk.CTkCanvas(root, width=495, height=430, bd=0, highlightthickness=0)
canvas.place(relx=0.21, rely=0.15, anchor="n")
bg_label = canvas.create_image(0, 0, anchor="nw", image=frames[0])

def update_gif():
    global frame_index
    frame_index = (frame_index + 1) % len(frames)
    canvas.itemconfig(bg_label, image=frames[frame_index])
    root.after(80, update_gif)

root.after(100, update_gif)

chat_frame = ctk.CTkScrollableFrame(root, width=480, height=390, fg_color="black")
chat_frame.place(x=470, rely=0.15)

entry = ctk.CTkEntry(root, width=430, placeholder_text="Type your message...")
entry.place(x=490, y=520)

speak_lock = threading.Lock()

def shorten_for_speech(text, max_paragraphs=2, max_chars=450):
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

def get_weather(city):
    api_key = "c5498e1c7df88bff8c847bfda5e406e8"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        data = requests.get(url).json()

        if data["cod"] != 200:
            return "City not found."

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        return f"Current weather in {city} is {temp} degree Celsius with {desc}"

    except Exception as e:
        print(e)
        return "Weather unavailable"    

def get_news():
    api_key = "0a97fed9720e7b5a5bd86acca0b5a65a"

    url = f"http://api.mediastack.com/v1/news?access_key={api_key}&countries=in&languages=en&sort=published_desc&limit=3"

    try:
        data = requests.get(url).json()
        articles = data["data"]

        if not articles:
            return "No latest news found."

        result = ""

        for i, article in enumerate(articles, 1):
            result += f"{i}. {article['title']} "

        return result

    except Exception as e:
        print(e)
        return "Unable to fetch news."              

def handle_commands(command):
    command = command.lower()

    if "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube"

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google"

    elif "open whatsapp" in command:
        webbrowser.open("https://web.whatsapp.com")
        return "Opening WhatsApp"

    elif "open notepad" in command:
        try:
            os.system("notepad.exe")
            return "Opening Notepad"
        except:
            return "Unable to open Notepad."

    elif "time" in command or "what's the time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}"
    
    elif "day" in command or "date" in command:
        today = datetime.datetime.now().strftime("Today is %A, %d %B, %Y")
        return today
    
    elif "volume up" in command:
     for _ in range(5):
        pyautogui.press("volumeup")
     return "Volume increased"

    elif "volume down" in command:
     for _ in range(5):
        pyautogui.press("volumedown")
     return "Volume decreased"

    elif "mute" in command:
     pyautogui.press("volumemute")
     return "Muted"
    
    elif "set brightness to" in command:
     try:
        value = int(command.split("to")[-1].strip().replace("%",""))
        sbc.set_brightness(value)
        return f"Brightness set to {value}%"
     except:
        return "Please specify a valid brightness level"
    
    elif "screenshot" in command:
     filename = f"screenshot_{datetime.datetime.now().strftime('%H%M%S')}.png"
     pyautogui.screenshot(filename)
     return f"Screenshot saved as {filename}"
    
    elif "play" in command:
     song = command.replace("play", "").strip()
    
     if song == "":
        return "What do you want me to play?"
    
     pywhatkit.playonyt(song)
     return f"Playing {song} on YouTube"
    
    elif "lock screen" in command:
     if platform.system() == "Windows":
        os.system("rundll32.exe user32.dll,LockWorkStation")
     return "Locking system"
    
    elif "stop" in command:
        global stop_speaking
        stop_speaking = True
        try:
          engine.stop()
        except:
            pass
        return "Okay, speech stopped!"
    
    elif "resume" in command:
        stop_speaking=False
        return"Yay! I'm back to speaking"
    
    elif "weather" in command or "temperature" in command:
    
     city = command.lower()

     words_to_remove = [
        "what is", "what's", "tell me", "show me",
        "weather", "temperature", "report", "in"
     ]

     for word in words_to_remove:
        city = city.replace(word, "")

     city = city.strip()

     if city == "":
        return "Please tell me the city name."

     return get_weather(city)
    
    elif "news" in command or "headlines" in command:
     return get_news()

    return None

def add_chat(name, message):
    if name.lower()=="you":
        label = ctk.CTkLabel(chat_frame, text=f"{name}:\n{message}",
                         anchor="e", justify="right", wraplength=300, font=("Arial", 14))
        label.pack(anchor="e", padx=13, pady=5,fill="x")
    else:
        label = ctk.CTkLabel(chat_frame, text=f"{name}:\n{message}",
                         anchor="w", justify="left", wraplength=300, font=("Arial", 14))
        label.pack(anchor="w", padx=13, pady=5,fill="x")

def get_response(event=None):
    user_input = entry.get().strip()
    if not user_input:
        return
    add_chat("You", user_input)
    entry.delete(0, "end")

    command_response = handle_commands(user_input)
    if command_response:
        add_chat("jarvis GPT", command_response)
        speak(command_response)
        return

    try:
        response = chat.send_message(user_input).text
    except Exception:
        response = "Oh nooo! jarvis GPT is tired! Try again in a bit."

    add_chat("jarvis GPT", response)
    speak(response)

def get_voice_input():
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

def process_image(image_path):
    try:
        img = Image.open(image_path)

        prompt = entry.get().strip()
        if not prompt:
            prompt = "Describe this image"

        add_chat("You", f"[Image Query]: {prompt}")
        entry.delete(0, "end")

        response = model.generate_content([prompt, img])
        result = response.text

    except Exception as e:
        print(e)
        result = "Image processing failed."

    add_chat("jarvis GPT", result)
    speak(result)  

def show_image_preview(path):
    img = Image.open(path)
    img.thumbnail((180, 180))
    img_tk = ImageTk.PhotoImage(img)

    label = ctk.CTkLabel(chat_frame, image=img_tk, text="")
    label.image = img_tk
    label.pack(anchor="e", padx=10, pady=5)          

def upload_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )    
    if not file_path:
        return
    
    add_chat("You", f"[Image uploaded: {os.path.basename(file_path)}]")

    show_image_preview(file_path)
    threading.Thread(target=process_image, args=(file_path,), daemon=True).start()      

send_button = ctk.CTkButton(root,text="⬆️",width=30,height=60,corner_radius=30,font=("Arial", 20),fg_color="#1f6aa5",hover_color="#144870",command=get_response)
send_button.place(x=490, y=560)

voice_button = ctk.CTkButton(root,text="🎤",width=30,height=60,corner_radius=30,font=("Arial", 20),fg_color="#1f6aa5",hover_color="#144870",command=lambda: threading.Thread(target=get_voice_input, daemon=True).start())
voice_button.place(x=710, y=560)

upload_btn = ctk.CTkButton(root,text="🖼️",width=30,height=60,corner_radius=30,command=upload_image)
upload_btn.place(x=600, y=560)

def wake_word_listener():
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

                root.after(1500,lambda: threading.Thread(target=get_voice_input,daemon=True).start())
        except:
            pass

def auto_greet():
    welcome_text = "Hello there! How can I help you today?"
    add_chat("jarvis GPT", welcome_text)
    speaker.Speak(welcome_text)

root.after(500, auto_greet)

root.after(1500, lambda: threading.Thread(target=wake_word_listener, daemon=True).start())
root.mainloop()