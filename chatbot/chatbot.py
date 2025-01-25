from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import httpx
import datetime
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Weather API Key (Replace with your own API Key)
WEATHER_API_KEY = "676b7afdeb994e90407ee7b5d4b91472"
WEATHER_API_URL = "http://api.openweathermap.org/data/2.5/forecast"

# Example project data (mock data for simplicity)
PROJECT_DATA = {
    1: {
        "name": "Highway Expansion",
        "start_date": "2025-01-20",
        "end_date": "2025-03-15",
        "tasks": [
            {"id": 101, "name": "Earthwork", "start_date": "2025-01-20", "duration_days": 10},
            {"id": 102, "name": "Pavement Layering", "start_date": "2025-02-01", "duration_days": 20},
        ],
    }
}

# Helper Function: Fetch Weather Data
async def fetch_weather(location: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{WEATHER_API_URL}?q={location}&appid={WEATHER_API_KEY}")
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.json()
        except httpx.RequestError as e:
            logger.error(f"Request error: {str(e)}")
            return {"error": f"Unable to fetch weather data: {str(e)}"}

# Helper Function: Predict Delays
def predict_delays(weather_data):
    delay_factors = {"rain": 2, "snow": 5, "clear": 0}  # Example delay factors (in days)
    total_delay = 0

    for day in weather_data.get("list", []):
        if "weather" in day and len(day["weather"]) > 0:
            weather_description = day["weather"][0].get("main", "").lower()
            if weather_description in delay_factors:
                total_delay += delay_factors[weather_description]

    return total_delay

# Helper Function: Reschedule Tasks
def reschedule_tasks(project_id, delay_days):
    project = PROJECT_DATA.get(project_id)
    if not project:
        return {"error": f"Project with ID {project_id} not found."}

    rescheduled_tasks = []
    for task in project["tasks"]:
        start_date = datetime.datetime.strptime(task["start_date"], "%Y-%m-%d")
        new_start_date = start_date + datetime.timedelta(days=delay_days)
        rescheduled_tasks.append({"task_id": task["id"], "new_start_date": new_start_date.strftime("%Y-%m-%d")})

    return {"project_name": project["name"], "rescheduled_tasks": rescheduled_tasks}

# Chatbot Endpoint
@app.post("/chatbot/")
async def chatbot(request: Request):
    data = await request.json()
    user_input = data.get("message")

    # Basic Chatbot Logic
    if "weather" in user_input.lower():
        location = user_input.split("in")[-1].strip()  # Extract location
        weather_data = await fetch_weather(location)
        if "error" in weather_data:
            return JSONResponse(content={"response": weather_data["error"]})

        return JSONResponse(content={"response": f"Weather data fetched for {location}. Use '/predict-delays/' for predictions."})

    elif "predict delays" in user_input.lower():
        location = user_input.split("in")[-1].strip()  # Extract location
        weather_data = await fetch_weather(location)
        if "error" in weather_data:
            return JSONResponse(content={"response": weather_data["error"]})

        delay_days = predict_delays(weather_data)
        return JSONResponse(content={"response": f"Predicted delay: {delay_days} days based on weather."})

    elif "reschedule" in user_input.lower():
        try:
            project_id = int(user_input.split("project")[-1].strip())
            delay_days = int(user_input.split("delay")[-1].split()[0])
        except (ValueError, IndexError):
            return JSONResponse(content={"response": "Invalid project ID or delay days. Please provide valid numbers."})

        reschedule_plan = reschedule_tasks(project_id, delay_days)

        if "error" in reschedule_plan:
            return JSONResponse(content={"response": reschedule_plan["error"]})

        return JSONResponse(content={
            "response": f"Tasks rescheduled for project: {reschedule_plan['project_name']}.",
            "rescheduled_tasks": reschedule_plan["rescheduled_tasks"]
        })

    else:
        return JSONResponse(content={"response": "Sorry, I didn't understand your request. Try asking about weather, predicting delays, or rescheduling tasks."})

# Run the application locally
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=3000)