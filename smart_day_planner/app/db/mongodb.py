from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from app.core.config import MONGO_URI, MONGO_DATABASE
from app.core.logger import get_logger
from typing import Optional, List
from datetime import datetime

logger = get_logger()

class MongoDB:
    """MongoDB database handler"""
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db = None
        self.users_collection = None
        self.plans_collection = None
        self.weather_logs_collection = None
    
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(MONGO_URI)
            self.db = self.client[MONGO_DATABASE]
            
            self.users_collection = self.db["users"]
            self.plans_collection = self.db["plans"]
            self.weather_logs_collection = self.db["weather_logs"]
            
            self.client.server_info()
            logger.info(f"Connected to MongoDB: {MONGO_DATABASE}")
            
            self._initialize_default_user()
            
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("Disconnected from MongoDB")
    
    def _initialize_default_user(self):
        """Create default user if not exists"""
        existing_user = self.users_collection.find_one({"user_id": "12345"})
        
        if not existing_user:
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
            self.users_collection.insert_one(default_user)
            logger.info("Default user created in MongoDB")
    
    def get_user_preferences(self, user_id: str = "12345") -> Optional[dict]:
        """Get user preferences"""
        try:
            user = self.users_collection.find_one({"user_id": user_id})
            if user:
                user.pop('_id', None)  
                return user
            return None
        except Exception as e:
            logger.error(f"Error getting user preferences: {e}")
            return None
    
    def update_user_preferences(self, user_id: str, preferences: dict) -> bool:
        """Update user preferences"""
        try:
            result = self.users_collection.update_one(
                {"user_id": user_id},
                {"$set": preferences},
                upsert=True
            )
            logger.info(f"User preferences updated for {user_id}")
            return result.acknowledged
        except Exception as e:
            logger.error(f"Error updating user preferences: {e}")
            return False
    
    def save_plan(self, plan: dict) -> bool:
        """Save a new plan"""
        try:
            self.plans_collection.insert_one(plan)
            logger.info(f"Plan saved for {plan['date']} - {plan['location']}")
            return True
        except Exception as e:
            logger.error(f"Error saving plan: {e}")
            return False
    
    def get_current_plan(self) -> Optional[dict]:
        """Get the most recent plan"""
        try:
            plan = self.plans_collection.find_one(
                sort=[("time_generated", -1)]
            )
            if plan:
                plan.pop('_id', None)
                return plan
            return None
        except Exception as e:
            logger.error(f"Error getting current plan: {e}")
            return None
    
    def get_plans_history(self, limit: int = 10) -> List[dict]:
        """Get recent plans history"""
        try:
            plans = list(
                self.plans_collection.find()
                .sort("time_generated", -1)
                .limit(limit)
            )
            for plan in plans:
                plan.pop('_id', None)
            return plans
        except Exception as e:
            logger.error(f"Error getting plans history: {e}")
            return []
    
    def log_weather(self, weather_data: dict) -> bool:
        """Log weather data"""
        try:
            log_entry = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                **weather_data
            }
            self.weather_logs_collection.insert_one(log_entry)
            logger.debug(f"Weather logged: {weather_data['city']} - {weather_data['condition']}")
            return True
        except Exception as e:
            logger.error(f"Error logging weather: {e}")
            return False
    
    def get_weather_logs(self, limit: int = 100) -> List[dict]:
        """Get recent weather logs"""
        try:
            logs = list(
                self.weather_logs_collection.find()
                .sort("timestamp", -1)
                .limit(limit)
            )
            for log in logs:
                log.pop('_id', None)
            return logs
        except Exception as e:
            logger.error(f"Error getting weather logs: {e}")
            return []

db = MongoDB()

def get_database() -> MongoDB:
    """Get database instance"""
    return db