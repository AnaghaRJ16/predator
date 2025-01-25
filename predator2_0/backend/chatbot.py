import json
from difflib import get_close_matches
import requests
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load the .env file to fetch the API key
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Load the knowledge base from a JSON file
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

# Save the knowledge base back to a JSON file
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)

# Find the closest match to the user's question
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Retrieve the weather and provide construction advice
def get_weather_with_advice(city: str) -> dict:
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return {"error": "API key not found. Please check your .env file."}

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"].lower()
            advice = (
                "The weather is not suitable for construction work. Please delay the work."
                if "rain" in weather_desc or "snow" in weather_desc or "storm" in weather_desc or temp < -5
                else "The weather is good. You can continue with the construction work."
            )
            return {
                "temperature": temp,
                "description": weather_desc,
                "advice": advice,
            }
        else:
            return {"error": "City not found. Please check the city name."}
    except Exception as e:
        return {"error": str(e)}

# API to process user input and respond
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").lower()

    # Load the knowledge base
    knowledge_base = load_knowledge_base("knowledge_base.json")

    # Handle weather-related queries
    if "weather" in user_input:
        city = user_input.replace("weather in", "").strip()
        weather_response = get_weather_with_advice(city)
        return jsonify(weather_response)

    # Find the best match in the knowledge base
    best_match = find_best_match(
        user_input, [q["question"] for q in knowledge_base["questions"]]
    )

    if best_match:
        answer = next(
            q["answer"]
            for q in knowledge_base["questions"]
            if q["question"] == best_match
        )
        return jsonify({"response": answer})
    else:
        return jsonify({"response": "I don't know the answer. Can you teach me?"})

# API to save new knowledge
@app.route("/teach", methods=["POST"])
def teach():
    data = request.json
    question = data.get("question")
    answer = data.get("answer")

    if question and answer:
        knowledge_base = load_knowledge_base("knowledge_base.json")
        knowledge_base["questions"].append({"question": question, "answer": answer})
        save_knowledge_base("knowledge_base.json", knowledge_base)
        return jsonify({"message": "Thank you! I learned a new response."})
    else:
        return jsonify({"error": "Both question and answer are required."}), 400

if __name__ == "__main__":
    app.run(debug=True)
