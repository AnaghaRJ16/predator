import json
from difflib import get_close_matches
import requests
import os
from dotenv import load_dotenv

# Load the .env file to fetch the API key
load_dotenv()

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_weather_with_advice(city: str) -> str:
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return "API key not found. Please check your .env file."

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            temp = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"].lower()

            if "rain" in weather_desc or "snow" in weather_desc or "storm" in weather_desc or temp < -5:
                advice = "The weather is not suitable for construction work. Please delay the work."
            else:
                advice = "The weather is good. You can continue with the construction work."

            return (
                f"The current temperature in {city} is {temp}°C with {weather_desc}. "
                f"{advice}"
            )
        else:
            return f"Sorry, I couldn't retrieve the weather for {city}. Please check the city name or try again later."
    except Exception as e:
        return f"An error occurred: {e}"