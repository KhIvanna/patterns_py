from datetime import datetime
from app.planner.strategies.sunny import SunnyWeatherStrategy
from app.planner.strategies.rainy import RainyWeatherStrategy
from app.planner.strategies.cloudy import CloudyWeatherStrategy
from app.planner.strategies.snowy import SnowyWeatherStrategy
from app.core.logger import get_logger

logger = get_logger()

class DayPlanner:
    """
    Context for Strategy Pattern + Observer for weather changes
    """
    
    def __init__(self, database, weather_station):
        self.db = database
        self.weather_station = weather_station
        self._strategy = None
        self.strategies = {
            'Sunny': SunnyWeatherStrategy(),
            'Rainy': RainyWeatherStrategy(),
            'Cloudy': CloudyWeatherStrategy(),
            'Snowy': SnowyWeatherStrategy()
        }
    
    def update(self, weather_data: dict):
        """
        Observer method - called when weather changes
        Regenerates the plan based on new weather
        """
        logger.info(f"DayPlanner received weather update: {weather_data['condition']}")
        
        try:
            user_prefs = self.db.get_user_preferences()
            self._generate_plan(weather_data, user_prefs)
        except Exception as e:
            logger.error(f"Error in observer update: {e}")
    
    def _generate_plan(self, weather_data: dict, user_prefs: dict):
        """Generate a new daily plan based on weather and preferences"""
        
        condition = weather_data['condition']
        self._strategy = self.strategies.get(condition, self.strategies['Cloudy'])
        
        logger.info(f"Using {self._strategy.__class__.__name__} for condition: {condition}")
        
        activities = self._strategy.get_activities(user_prefs['preferences'])
        
        plan = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time_generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "location": weather_data['city'],
            "weather": {
                "condition": weather_data['condition'],
                "temperature": weather_data['temperature'],
                "description": weather_data['description']
            },
            "activities": activities,
            "user_id": user_prefs['user_id']
        }
        
        self.db.save_plan(plan)
        
        logger.info(
            f"Plan generated: {len(activities)} activities for {condition} weather in {weather_data['city']}"
        )
        
        return plan