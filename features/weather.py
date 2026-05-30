import requests
from config import WEATHER_API_KEY

def get_weather(city):
    api_key = WEATHER_API_KEY

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