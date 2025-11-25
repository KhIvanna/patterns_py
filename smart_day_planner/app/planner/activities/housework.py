from app.planner.activities.base import Activity

class HouseWork(Activity):
    """HouseWork activity for indoor days"""
    
    def __init__(self):
        super().__init__(
            name="HouseWork",
            activity_type="indoor",
            priority=5
        )
    
    def get_description(self) -> str:
        return "Clean house, organize rooms, do laundry"