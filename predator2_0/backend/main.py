from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = FastAPI()

# Define request and response models
class WeatherRequest(BaseModel):
    city: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Weather API!"}

@app.post("/get_weather")
def get_weather(request: WeatherRequest):
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not found")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={request.city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"].lower()
            advice = "Suitable for construction" if "rain" not in weather_desc else "Not suitable for construction"
            return {
                "city": request.city,
                "temperature": temp,
                "description": weather_desc,
                "advice": advice,
            }
        else:
            raise HTTPException(status_code=404, detail="City not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
