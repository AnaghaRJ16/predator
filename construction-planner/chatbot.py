from flask import Flask, request, jsonify
from src.api.accuweather import get_weather_data
from src.api.gpt_utils import generate_ai_response
from src.budget_analysis.budget_model import predict_budget
from src.budget_analysis.risk_analysis import analyze_risk, predictive_delay_modeling, dynamic_rescheduling, what_if_scenarios, resource_optimization, real_time_adjustments
from src.visualization.dashboard import get_dashboard_link

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Determine intent based on user input (simplified for now)
    if "weather" in user_message.lower():
        location = extract_location(user_message)
        if not location:
            return jsonify({"response": "Please specify a location for weather information."})
        weather_data = get_weather_data(location)
        return jsonify({"response": f"The weather in {location} is {weather_data}"})

    elif "budget" in user_message.lower():
        project_details = extract_project_details(user_message)
        if not project_details:
            return jsonify({"response": "Please provide details about the project for budget analysis."})
        budget = predict_budget(project_details)
        return jsonify({"response": f"The estimated budget for your project is ${budget}"})

    elif "risk" in user_message.lower():
        zone = extract_zone(user_message)
        if not zone:
            return jsonify({"response": "Please specify the construction zone for risk analysis."})
        
        risk_profile = analyze_risk(zone)
        delay_prediction = predictive_delay_modeling(zone)
        rescheduling_plan = dynamic_rescheduling(zone)
        what_if = what_if_scenarios(zone)
        optimization = resource_optimization(zone)
        real_time_update = real_time_adjustments(zone)
        
        fixes = (
            "To mitigate delays:\n"
            "- Prioritize indoor or unaffected tasks.\n"
            "- Utilize protective measures for materials.\n"
            "- Allocate additional resources post-storm.\n"
            "- Use real-time updates for proactive adjustments."
        )
        return jsonify({"response": f"Risk Analysis for {zone}:\n"
                                    f"- Risk Profile: {risk_profile}\n"
                                    f"- Predicted Delays: {delay_prediction}\n"
                                    f"- Rescheduling Plan: {rescheduling_plan}\n"
                                    f"- What-If Scenarios: {what_if}\n"
                                    f"- Resource Optimization: {optimization}\n"
                                    f"- Real-Time Adjustments: {real_time_update}\n\n"
                                    f"{fixes}"})

    elif "dashboard" in user_message.lower():
        dashboard_link = get_dashboard_link()
        return jsonify({"response": f"You can view the project dashboard here: {dashboard_link}"})

    else:
        ai_response = generate_ai_response(user_message)
        return jsonify({"response": ai_response})

# Utility functions (to be implemented)
def extract_location(message):
    # Parse location from user message
    return "New York"  # Placeholder

def extract_project_details(message):
    # Parse project details from user message
    return {"size": 1000, "materials": ["steel", "concrete"]}  # Placeholder

def extract_zone(message):
    # Parse construction zone from user message
    return "Zone A"  # Placeholder

if __name__ == "__main__":
    app.run(debug=True)
