from flask import Flask, request, jsonify
from flask_cors import CORS
from chatbot import load_knowledge_base, find_best_match, get_weather_with_advice
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    
    if "weather" in user_input:
        city = user_input.replace("weather in", "").strip()
        response = get_weather_with_advice(city)
    else:
        # Load knowledge base and find the best match
        knowledge_base = load_knowledge_base("knowledge_base.json")
        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
        
        if best_match:
            answer = next(q["answer"] for q in knowledge_base["questions"] if q["question"] == best_match)
            response = answer
        else:
            response = "I don't know the answer. Can you teach me?"
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)