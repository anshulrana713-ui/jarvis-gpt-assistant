from features.media import (
    open_youtube,
    open_google,
    open_whatsapp,
    play_song
)
from features.system_controls import (
    volume_up,
    volume_down,
    mute_volume,
    set_brightness,
    take_screenshot,
    lock_screen
)
from features.weather import get_weather
from features.news import get_news
import os
import datetime

def handle_commands(command):
    command = command.lower()
    
    if "open youtube" in command:
       return open_youtube()

    elif "open google" in command:
         return open_google()

    elif "open whatsapp" in command:
         return open_whatsapp()

    elif "play" in command:
         song = command.replace("play", "").strip()
         return play_song(song)

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
         return volume_up()

    elif "volume down" in command:
        return volume_down()

    elif "mute" in command:
        return mute_volume()

    elif "set brightness to" in command:
        return set_brightness(command)

    elif "screenshot" in command:
        return take_screenshot()

    elif "lock screen" in command:
        return lock_screen()
    
    elif "stop" in command:
        return "Okay, speech stopped!"
    
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