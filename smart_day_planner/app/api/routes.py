from fastapi import APIRouter, HTTPException
from app.planner.day_planner import DayPlanner
from app.weather.weather_station import WeatherStation
from app.db.mongodb import get_database
from app.core.logger import get_logger
from pydantic import BaseModel
from typing import Optional

router = APIRouter()
logger = get_logger()

db = get_database()
weather_station = WeatherStation()
day_planner = DayPlanner(db, weather_station)

weather_station.attach(day_planner)

class PreferencesUpdate(BaseModel):
    preferred_types: list[str]
    avoid_types: list[str]
    working_hours: dict
    weekend_mode: str

class LocationUpdate(BaseModel):
    city: str

@router.get("/plan/current")
async def get_current_plan():
    """Get the current day plan"""
    try:
        plan = db.get_current_plan()
        if not plan:
            user_prefs = db.get_user_preferences()
            weather_station.fetch_weather(user_prefs.get("location", "Lviv"))
            plan = db.get_current_plan()
        
        return {"success": True, "plan": plan}
    except Exception as e:
        logger.error(f"Error fetching current plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/weather/update")
async def update_weather(location: Optional[LocationUpdate] = None):
    """Force weather update and regenerate plan"""
    try:
        user_prefs = db.get_user_preferences()
        city = location.city if location else user_prefs.get("location", "Lviv")
        
        logger.info(f"Forcing weather update for {city}")
        weather_station.fetch_weather(city)
        
        plan = db.get_current_plan()
        return {
            "success": True, 
            "message": "Weather updated and plan regenerated",
            "plan": plan
        }
    except Exception as e:
        logger.error(f"Error updating weather: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preferences")
async def get_preferences():
    """Get user preferences"""
    try:
        prefs = db.get_user_preferences()
        return {"success": True, "preferences": prefs}
    except Exception as e:
        logger.error(f"Error fetching preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/preferences")
async def update_preferences(prefs: PreferencesUpdate):
    """Update user preferences"""
    try:
        current_prefs = db.get_user_preferences()
        
        updated_prefs = {
            **current_prefs,
            "preferences": {
                "preferred_types": prefs.preferred_types,
                "avoid_types": prefs.avoid_types,
                "working_hours": prefs.working_hours,
                "weekend_mode": prefs.weekend_mode
            }
        }
        
        db.update_user_preferences("12345", updated_prefs)
        
        weather_station.fetch_weather(current_prefs.get("location", "Lviv"))
        
        logger.info("Preferences updated and plan regenerated")
        return {
            "success": True, 
            "message": "Preferences updated",
            "preferences": updated_prefs
        }
    except Exception as e:
        logger.error(f"Error updating preferences: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/plans/history")
async def get_plans_history():
    """Get historical plans"""
    try:
        history = db.get_plans_history()
        return {"success": True, "history": history}
    except Exception as e:
        logger.error(f"Error fetching plans history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/weather/current")
async def get_current_weather():
    """Get current weather data"""
    try:
        weather = weather_station.get_current_weather()
        return {"success": True, "weather": weather}
    except Exception as e:
        logger.error(f"Error fetching weather: {e}")
        raise HTTPException(status_code=500, detail=str(e))