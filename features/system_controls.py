import pyautogui
import datetime
import platform
import os
import screen_brightness_control as sbc

def volume_up():
    for _ in range(5):
        pyautogui.press("volumeup")

    return "Volume increased"

def volume_down():
    for _ in range(5):
        pyautogui.press("volumedown")

    return "Volume decreased"

def mute_volume():
    pyautogui.press("volumemute")
    return "Muted"

def set_brightness(command):
    try:
        value = int(command.split("to")[-1].strip().replace("%", ""))

        sbc.set_brightness(value)

        return f"Brightness set to {value}%"

    except:
        return "Please specify a valid brightness level"

def take_screenshot():
    filename = f"screenshot_{datetime.datetime.now().strftime('%H%M%S')}.png"

    pyautogui.screenshot(filename)

    return f"Screenshot saved as {filename}"

def lock_screen():
    if platform.system() == "Windows":
        os.system("rundll32.exe user32.dll,LockWorkStation")

    return "Locking system"