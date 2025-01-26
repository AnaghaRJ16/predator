<<<<<<< HEAD
from src.visualization.dashboard import Dashboard
import tkinter as tk
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def main():
    # Retrieve API keys and data paths from environment variables
    weather_api_key = os.getenv('ACC_WEATHER_API_KEY')
    project_data_file = 'data/projects.json'

    if not weather_api_key:
        print("Error: Weather API key is missing.")
        return

    # Initialize Tkinter root window
    root = tk.Tk()

    # Create and configure the dashboard with the weather API key and project data file
    dashboard = Dashboard(root, weather_api_key, project_data_file)

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()
=======
from chatbot import app as chatbot_app

if __name__ == "__main__":
    chatbot_app.run(debug=True)
>>>>>>> 748b049a15ec9d10a124b941eb3dbc182efdefbe
