from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow requests from the frontend

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if not city:
        return jsonify({"error": "City is required"}), 400

    api_key = os.getenv("e4e4d33fab5f98bb71f75485b9ab3f99")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data['main']['temp']
            weather_desc = data['weather'][0]['description']

            advice = "Good for construction work" if temp > 0 and "rain" not in weather_desc.lower() else "Not suitable for construction"
            return jsonify({
                "city": city,
                "temperature": temp,
                "description": weather_desc,
                "advice": advice
            })
        else:
            return jsonify({"error": "City not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
