from app.planner.activities.base import Activity

class Studying(Activity):
    """Studying activity"""
    
    def __init__(self):
        super().__init__(
            name="Studying",
            activity_type="productive",
            priority=4
        )
    
    def get_description(self) -> str:
        return "Study for exams, work on assignments, learn new material"