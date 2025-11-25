from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class UserPreferences(BaseModel):
    """User preferences model"""
    preferred_types: List[str] = Field(default=["outdoor", "learning"])
    avoid_types: List[str] = Field(default=["sport"])
    working_hours: dict = Field(default={"start": 9, "end": 17})
    weekend_mode: str = Field(default="Always relax on Sundays")

class User(BaseModel):
    """User model"""
    user_id: str
    location: str = Field(default="Lviv")
    preferences: UserPreferences

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "12345",
                "location": "Lviv",
                "preferences": {
                    "preferred_types": ["outdoor", "learning"],
                    "avoid_types": ["sport"],
                    "working_hours": {"start": 9, "end": 17},
                    "weekend_mode": "Always relax on Sundays"
                }
            }
        }

class Weather(BaseModel):
    """Weather information model"""
    condition: str
    temperature: int
    description: str

class Activity(BaseModel):
    """Activity model"""
    name: str
    type: str
    priority: int

class Plan(BaseModel):
    """Daily plan model"""
    date: str
    time_generated: str
    location: str
    weather: Weather
    activities: List[Activity]
    user_id: str

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2025-11-20",
                "time_generated": "2025-11-20 08:00:00",
                "location": "Lviv",
                "weather": {
                    "condition": "Cloudy",
                    "temperature": 3,
                    "description": "overcast clouds"
                },
                "activities": [
                    {"name": "Shopping", "type": "outdoor", "priority": 4},
                    {"name": "Museum Visit", "type": "learning", "priority": 4}
                ],
                "user_id": "12345"
            }
        }

class WeatherLog(BaseModel):
    """Weather log model"""
    timestamp: str
    city: str
    condition: str
    temperature: int
    description: str
    humidity: int