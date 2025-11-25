from app.planner.activities.base import Activity

class Date(Activity):
    """Date activity"""
    
    def __init__(self):
        super().__init__(
            name="Date",
            activity_type="indoor",
            priority=3
        )
    
    def get_description(self) -> str:
        return "Go on a date, romantic dinner, quality time together"