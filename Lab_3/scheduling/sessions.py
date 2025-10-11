from abc import ABC, abstractmethod
from typing import Optional
from .teachers import Teacher, Lecturer, Assistant, ExternalMentor

class ClassSession(ABC):
    """
    Abstract Session (Product in Factory Method).
    Responsible for session details and validating teacher assignment (SRP).
    """
    def __init__(self, time: str, room: str, teacher: Optional[Teacher] = None):
        self.time = time
        self.room = room
        self._teacher = teacher
        self._validate_teacher_assignment()

    @property
    def teacher(self) -> Optional[Teacher]:
        return self._teacher
    
    @teacher.setter
    def teacher(self, new_teacher: Teacher):
        """Setter ensures teacher validity before assignment."""
        self._teacher = new_teacher
        self._validate_teacher_assignment()

    def _validate_teacher_assignment(self):
        """Ensures that the assigned teacher is qualified for the session type."""
        if self._teacher and not self._teacher.can_teach(self.get_session_type()):
            raise ValueError(
                f"{self._teacher.__class__.__name__} '{self._teacher.name}' "
                f"cannot teach a {self.get_session_type()}."
            )

    @abstractmethod
    def get_session_type(self) -> str:
        """Returns the session type for teacher capability checking."""
        pass
    
    def __repr__(self):
        teacher_name = self.teacher.name if self.teacher else "Unassigned"
        return f"{self.get_session_type()}Session(time='{self.time}', room='{self.room}', teacher='{teacher_name}')"

class LectureSession(ClassSession):
    """Concrete Session: Lecture."""
    def get_session_type(self) -> str:
        return "Lecture"

class PracticalSession(ClassSession):
    """Concrete Session: Practical."""
    def get_session_type(self) -> str:
        return "Practical"

class ProgrammingLecture(LectureSession):
    pass

class ProgrammingPractical(PracticalSession):
    pass