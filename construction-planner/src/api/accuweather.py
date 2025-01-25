import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")
CACHE_FILE = "data/weather_cache.json"


def fetch_weather_data(lat, lon):
    """
    Fetch 10-day weather forecast data from OpenWeather API.
    
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
    
    Returns:
        dict: Processed weather forecast data.
    """
    url = f"https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "lat": lat,
        "lon": lon,
        "appid": API_KEY,
        "units": "metric",  # Use metric system (Celsius, etc.)
    }
    
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        forecast_data = response.json()
        return process_weather_data(forecast_data)
    else:
        raise Exception(f"OpenWeather API error: {response.status_code} - {response.text}")


def process_weather_data(data):
    """
    Process raw weather data from OpenWeather API to extract relevant information.
    
    Args:
        data (dict): Raw weather data from OpenWeather API.
    
    Returns:
        list: Processed weather data for 10 days, including temperature, conditions, etc.
    """
    daily_weather = {}
    
    # Loop through each 3-hour forecast and group by day
    for entry in data['list']:
        date = entry['dt_txt'].split(" ")[0]  # Extract the date
        if date not in daily_weather:
            daily_weather[date] = {
                "date": date,
                "temperatures": [],
                "conditions": [],
            }
        
        # Add temperature and weather condition for this 3-hour block
        daily_weather[date]["temperatures"].append(entry["main"]["temp"])
        daily_weather[date]["conditions"].append(entry["weather"][0]["description"])
    
    # Summarize daily weather data
    summarized_weather = []
    for day in daily_weather.values():
        summarized_weather.append({
            "date": day["date"],
            "average_temp": sum(day["temperatures"]) / len(day["temperatures"]),
            "conditions": max(set(day["conditions"]), key=day["conditions"].count),  # Most common condition
        })
    
    return summarized_weather[:10]  # Limit to 10 days


def cache_weather_data(lat, lon, weather_data):
    """
    Cache the weather data into a JSON file.
    
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        weather_data (list): Processed weather data.
    """
    cache = load_weather_cache()
    location_key = f"{lat},{lon}"
    cache[location_key] = {
        "data": weather_data,
        "timestamp": datetime.now().isoformat(),
    }
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=4)


def load_weather_cache():
    """
    Load cached weather data from a JSON file.
    
    Returns:
        dict: Cached weather data.
    """
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}


def get_weather(lat, lon):
    """
    Get weather data for a location, either from cache or by making an API call.
    
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
    
    Returns:
        list: Processed weather forecast data.
    """
    cache = load_weather_cache()
    location_key = f"{lat},{lon}"
    
    # Check if the data is in cache and is less than 6 hours old
    if location_key in cache:
        cached_entry = cache[location_key]
        timestamp = datetime.fromisoformat(cached_entry["timestamp"])
        if datetime.now() - timestamp < timedelta(hours=6):
            print("Using cached weather data.")
            return cached_entry["data"]
    
    # Fetch fresh weather data
    print("Fetching fresh weather data from OpenWeather API.")
    weather_data = fetch_weather_data(lat, lon)
    cache_weather_data(lat, lon, weather_data)
    return weather_data


if __name__ == "__main__":
    # Example usage
    # Replace with the desired latitude and longitude
    latitude = 40.7128  # Example: New York City latitude
    longitude = -74.0060  # Example: New York City longitude
    
    try:
        weather_forecast = get_weather(latitude, longitude)
        print("10-Day Weather Forecast:")
        for day in weather_forecast:
            print(f"Date: {day['date']}, Avg Temp: {day['average_temp']}°C, Conditions: {day['conditions']}")
    except Exception as e:
        print(f"Error fetching weather data: {e}")
