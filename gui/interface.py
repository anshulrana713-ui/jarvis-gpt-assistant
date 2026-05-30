import customtkinter as ctk
from PIL import Image, ImageTk, ImageSequence
import threading
from config import *
from core.speech_engine import speak
from core.listener import get_voice_input
from tkinter import filedialog
import threading
import os
from features.vision import process_image
from core.command_handler import handle_commands
from core.speech_engine import speak
from core.assistant import get_ai_response

def create_gui():

  ctk.set_appearance_mode(THEME_MODE)
  ctk.set_default_color_theme(COLOR_THEME)

  root = ctk.CTk()
  root.title(WINDOW_TITLE)
  root.geometry(WINDOW_SIZE)

  title_label = ctk.CTkLabel(root, text="jarvis GPT", font=("Comic Sans MS", 35, "bold"))
  title_label.place(relx=0.5, rely=0.04, anchor="center")

  gif_path = GIF_PATH
  gif = Image.open(gif_path)
  frames = [ImageTk.PhotoImage(frame.convert("RGBA")) for frame in ImageSequence.Iterator(gif)]

  canvas = ctk.CTkCanvas(root, width=495, height=430, bd=0, highlightthickness=0)
  canvas.place(relx=0.21, rely=0.15, anchor="n")
  bg_label = canvas.create_image(0, 0, anchor="nw", image=frames[0])

  frame_index = 0
  
  def update_gif():
    nonlocal frame_index
    frame_index = (frame_index + 1) % len(frames)
    canvas.itemconfig(bg_label, image=frames[frame_index])
    root.after(GIF_SPEED, update_gif)

  root.after(100, update_gif)

  chat_frame = ctk.CTkScrollableFrame(root, width=480, height=390, fg_color="black")
  chat_frame.place(x=470, rely=0.15)

  entry = ctk.CTkEntry(root, width=430, placeholder_text="Type your message...")
  entry.place(x=490, y=520)

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
        response = get_ai_response(user_input)
    except Exception:
        response = "Oh nooo! jarvis GPT is tired! Try again in a bit."

    add_chat("jarvis GPT", response)
    speak(response) 

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

    prompt = entry.get().strip()
    entry.delete(0, "end")

    show_image_preview(file_path)
    threading.Thread(target=process_image, args=(file_path, prompt, add_chat, speak), daemon=True).start()
   
  send_button = ctk.CTkButton(root,text="⬆️",width=30,height=60,corner_radius=30,font=("Arial", 20),fg_color="#1f6aa5",hover_color="#144870",command=get_response)
  send_button.place(x=490, y=560)

  voice_button = ctk.CTkButton(root,text="🎤",width=30,height=60,corner_radius=30,font=("Arial", 20),fg_color="#1f6aa5",hover_color="#144870",command=lambda: threading.Thread(target=get_voice_input,args=(root, add_chat, entry, get_response),daemon=True).start())
  voice_button.place(x=710, y=560)

  upload_btn = ctk.CTkButton(root,text="🖼️",width=30,height=60,corner_radius=30,command=upload_image)
  upload_btn.place(x=600, y=560)

  return root, add_chat, entry, get_response