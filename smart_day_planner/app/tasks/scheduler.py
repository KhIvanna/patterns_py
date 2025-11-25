import asyncio
from app.weather.weather_station import WeatherStation
from app.db.mongodb import get_database
from app.core.logger import get_logger

logger = get_logger()

async def check_weather_periodically():
    """Background task to check weather every 30 minutes"""
    
    db = get_database()
    weather_station = WeatherStation()
    
    while True:
        try:
            user_prefs = db.get_user_preferences()
            city = user_prefs.get("location", "Lviv")
            
           
            logger.info(f"[BACKGROUND] Checking weather for {city}")
            weather_station.fetch_weather(city)
            
            await asyncio.sleep(1800) 
            
        except Exception as e:
            logger.error(f"[BACKGROUND] Error in weather check: {e}")
            await asyncio.sleep(60)