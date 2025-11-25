from app.planner.activities.base import Activity

class Hiking(Activity):
    """Biking activity for sunny weather"""
    
    def __init__(self):
        super().__init__(
            name="Hiking",
            activity_type="outdoor",
            priority=4
        )
    
    def get_description(self) -> str:
        return "hiking in the mountains"