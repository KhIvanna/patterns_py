from app.planner.strategies.base import WeatherStrategy
from typing import List, Dict

class SunnyWeatherStrategy(WeatherStrategy):
    """Strategy for sunny weather - outdoor activities"""
    
    def get_activities(self, user_preferences: dict) -> List[Dict]:
        """Generate outdoor activities for sunny weather"""
        
        activities = [
            {"name": "Hiking", "type": "outdoor", "priority": 5},
            {"name": "Sport", "type": "outdoor", "priority": 4},
            {"name": "Date", "type": "outdoor", "priority": 3},
        ]
        
        filtered = self._filter_by_preferences(activities, user_preferences)
        sorted_activities = self._sort_by_priority(filtered)
        
        return sorted_activities[:5]