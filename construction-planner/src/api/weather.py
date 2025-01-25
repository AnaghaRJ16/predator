import requests
import json
from dotenv import load_dotenv
import os

# Load API key from environment variables
load_dotenv()
API_KEY = os.getenv("3053bc4be8e042c6ae590222252501")
BASE_URL = "http://weather.com/"

def get_weather_data(city_id):
    """
    Fetch weather data for a given city using AccuWeather API.
    """
    url = f"{BASE_URL}/currentconditions/v1/{city_id}?apikey={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to fetch data"}
