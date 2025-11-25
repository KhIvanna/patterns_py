import json
import os
from typing import Optional, List
from datetime import datetime
from app.core.logger import get_logger

logger = get_logger()

class JsonDatabase:
    """Simple JSON-based database"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        self.plans_file = os.path.join(data_dir, "plans.json")
        self.weather_file = os.path.join(data_dir, "weather_logs.json")
        
        os.makedirs(data_dir, exist_ok=True)
        
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialize JSON files with default data"""
        
        if not os.path.exists(self.users_file):
            default_user = {
                "user_id": "12345",
                "location": "Lviv",
                "preferences": {
                    "preferred_types": ["outdoor", "learning"],
                    "avoid_types": ["sport"],
                    "working_hours": {"start": 9, "end": 17},
                    "weekend_mode": "Always relax on Sundays"
                }
            }
            self._write_json(self.users_file, default_user)
            logger.info("Initialized users.json with default data")
        
        if not os.path.exists(self.plans_file):
            self._write_json(self.plans_file, [])
            logger.info("Initialized plans.json")
        
        if not os.path.exists(self.weather_file):
            self._write_json(self.weather_file, [])
            logger.info("Initialized weather_logs.json")
    
    def _read_json(self, filepath: str):
        """Read JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading {filepath}: {e}")
            return None
    
    def _write_json(self, filepath: str, data):
        """Write JSON file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            logger.error(f"Error writing {filepath}: {e}")
            return False
    
    def get_user_preferences(self) -> dict:
        """Get user preferences"""
        return self._read_json(self.users_file)
    
    def update_user_preferences(self, preferences: dict):
        """Update user preferences"""
        success = self._write_json(self.users_file, preferences)
        if success:
            logger.info("User preferences updated")
        return success
    
    def save_plan(self, plan: dict):
        """Save a new plan to plans history"""
        plans = self._read_json(self.plans_file) or []
        plans.append(plan)
        
        if len(plans) > 30:
            plans = plans[-30:]
        
        success = self._write_json(self.plans_file, plans)
        if success:
            logger.info(f"Plan saved for {plan['date']} - {plan['location']}")
        return success
    
    def get_current_plan(self) -> Optional[dict]:
        """Get the most recent plan"""
        plans = self._read_json(self.plans_file) or []
        if plans:
            return plans[-1]
        return None
    
    def get_plans_history(self, limit: int = 10) -> List[dict]:
        """Get recent plans history"""
        plans = self._read_json(self.plans_file) or []
        return plans[-limit:]
    
    def log_weather(self, weather_data: dict):
        """Log weather data"""
        logs = self._read_json(self.weather_file) or []
        
        log_entry = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            **weather_data
        }
        
        logs.append(log_entry)
        
        if len(logs) > 100:
            logs = logs[-100:]
        
        self._write_json(self.weather_file, logs)
        logger.debug(f"Weather logged: {weather_data['city']} - {weather_data['condition']}")