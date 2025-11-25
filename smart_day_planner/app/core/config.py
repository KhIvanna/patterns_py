import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY", "YOUR_API_KEY_HERE")
WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"

APP_NAME = "Smart Day Planner"
APP_VERSION = "1.0.0"

MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "smart_planner")
MONGO_URI = f"mongodb://{MONGO_HOST}:{MONGO_PORT}/"

WEATHER_CHECK_INTERVAL = 1800 