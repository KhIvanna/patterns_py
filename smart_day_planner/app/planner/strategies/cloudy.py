from app.planner.strategies.base import WeatherStrategy
from typing import List, Dict

class CloudyWeatherStrategy(WeatherStrategy):
    """Strategy for cloudy weather - mixed activities"""
    
    def get_activities(self, user_preferences: dict) -> List[Dict]:
        """Generate mixed indoor/outdoor activities for cloudy weather"""
        
        activities = [
            {"name": "Studying", "type": "productive", "priority": 4},
            {"name": "Sport", "type": "indoor", "priority": 3},
            {"name": "Date", "type": "indoor", "priority": 3},
        ]
        
        filtered = self._filter_by_preferences(activities, user_preferences)
        sorted_activities = self._sort_by_priority(filtered)
        
        return sorted_activities[:5]