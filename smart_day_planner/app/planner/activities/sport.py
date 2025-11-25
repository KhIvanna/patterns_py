from app.planner.activities.base import Activity

class Sport(Activity):
    """Sport activity for outdoor days"""
    
    def __init__(self):
        super().__init__(
            name="Sport",
            activity_type="outdoor",
            priority=4
        )
    
    def get_description(self) -> str:
        return "Play sports, go to gym, outdoor exercises"