from app.planner.strategies.base import WeatherStrategy
from typing import List, Dict

class SnowyWeatherStrategy(WeatherStrategy):
    """Strategy for snowy weather - winter activities"""
    
    def get_activities(self, user_preferences: dict) -> List[Dict]:
        """Generate winter activities for snowy weather"""
        
        activities = [
            {"name": "HouseWork", "type": "indoor", "priority": 5},
            {"name": "Studying", "type": "productive", "priority": 4},
            {"name": "Date", "type": "indoor", "priority": 3},
        ]
        
        filtered = self._filter_by_preferences(activities, user_preferences)
        sorted_activities = self._sort_by_priority(filtered)
        
        return sorted_activities[:5]