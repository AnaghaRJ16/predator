import json
from difflib import get_close_matches
import requests  # Import requests for API calls
import os
from dotenv import load_dotenv
import json

# Embed the JSON data directly in the Python script
knowledge_base = {
    "questions": [
        {
            "question": "delhi",
            "answer": ""
        }
    ]
}

def find_answer(question):
    # Loop through the questions and return the answer if found
    for entry in knowledge_base["questions"]:
        if entry["question"].lower() == question.lower():
            return entry["answer"]
    return "Question not found in the knowledge base."

# Example usage
user_input = "delhi"
response = find_answer(user_input)
print(response)  # Output: "skip"
# Load the .env file to fetch the API key
load_dotenv()

# Function to load the knowledge base from JSON
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

# Function to save the knowledge base back to JSON
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=2)

# Function to find the closest match
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Function to retrieve the weather and provide construction advice
def get_weather_with_advice(city: str) -> str:
    api_key = os.getenv("WEATHER_API_KEY")  # Fetch the API key from .env
    if not api_key:
        return "API key not found. Please check your .env file."

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            temp = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"].lower()

            # Determine if the weather is suitable for construction
            if "rain" in weather_desc or "snow" in weather_desc or "storm" in weather_desc or "scattered clouds" in weather_desc or temp<-5:
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

# Main chatbot function
def chatbot():
   # knowledge_base = load_knowledge_base("knowledge_base.json")
    
    while True:
        user_input = input("You: ").lower()
        if user_input == "quit":
            break
        
        # Check if the user is asking about the weather
        if "weather" in user_input:
            city = user_input.replace("weather in", "").strip()
            weather_response = get_weather_with_advice(city)
            print(f"Bot: {weather_response}")
            continue
        
        best_match = find_best_match(
            user_input, 
            [q["question"] for q in knowledge_base["questions"]]
        )
        
        if best_match:
            answer = next(q["answer"] for q in knowledge_base["questions"] if q["question"] == best_match)
            print(f"Bot: {answer}")
        else:
            print("Bot: I don't know the answer. Can you teach me?")
            new_answer = input("Type the answer (or type 'skip' to skip): ").lower()
            
            if new_answer != "skip":
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base("knowledge_base.json", knowledge_base)
                print("Bot: Thank you! I learned a new response.")

# Entry point
if __name__ == "__main__":
    chatbot()
