import google.generativeai as ai
from config import *

ai.configure(api_key="GEMINI_API_KEY")
model = ai.GenerativeModel(model_name="MODEL_NAME")
chat = model.start_chat()

def generate_image_response(prompt, image):
    response = model.generate_content([prompt, image])
    return response.text

def get_ai_response(prompt):
    """
    Sends user message to Gemini
    and returns AI response.
    """

    try:
        response = chat.send_message(prompt)
        return response.text

    except Exception as e:
        print("AI Error:", e)
        return "Sorry, I couldn't process that request."
    
