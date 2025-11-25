from abc import ABC, abstractmethod
from typing import List, Dict

class WeatherStrategy(ABC):
    """Abstract base class for weather strategies"""
    
    @abstractmethod
    def get_activities(self, user_preferences: dict) -> List[Dict]:
        """
        Generate activities based on weather and user preferences
        
        Args:
            user_preferences: dict with preferred_types, avoid_types, working_hours, weekend_mode
            
        Returns:
            List of activities with name, type, and priority
        """
        pass
    
    def _filter_by_preferences(self, activities: List[Dict], preferences: dict) -> List[Dict]:
        """
        Filter activities based on user preferences
        
        Removes activities that:
        - Are in avoid_types
        - Don't match preferred_types (if specified)
        """
        avoid_types = preferences.get('avoid_types', [])
        preferred_types = preferences.get('preferred_types', [])
        
        filtered = []
        for activity in activities:
            if activity['type'] in avoid_types:
                continue
            
            if preferred_types and activity['type'] not in preferred_types:
                continue
            
            filtered.append(activity)
        
        return filtered
    
    def _sort_by_priority(self, activities: List[Dict]) -> List[Dict]:
        """Sort activities by priority (higher priority first)"""
        return sorted(activities, key=lambda x: x['priority'], reverse=True)