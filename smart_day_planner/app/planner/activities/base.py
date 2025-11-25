from abc import ABC, abstractmethod
from typing import Dict

class Activity(ABC):
    """Base class for all activities"""
    
    def __init__(self, name: str, activity_type: str, priority: int):
        self.name = name
        self.type = activity_type
        self.priority = priority
    
    def to_dict(self) -> Dict:
        """Convert activity to dictionary"""
        return {
            "name": self.name,
            "type": self.type,
            "priority": self.priority
        }
    
    @abstractmethod
    def get_description(self) -> str:
        """Get activity description"""
        pass