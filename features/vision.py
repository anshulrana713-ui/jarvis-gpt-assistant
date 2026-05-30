from core.assistant import generate_image_response
from PIL import Image

def process_image(image_path, prompt, add_chat, speak):
    try:
        img = Image.open(image_path)

        if not prompt.strip():
            prompt = "Describe this image"

        add_chat("You", f"[Image Query]: {prompt}")

        result = generate_image_response(prompt, img)

    except Exception as e:
        print(e)
        result = "Image processing failed."

    add_chat("jarvis GPT", result)
    speak(result)  

