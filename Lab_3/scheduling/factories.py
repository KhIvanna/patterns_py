from abc import ABC, abstractmethod
from .sessions import ClassSession, LectureSession, PracticalSession

class SessionFactory(ABC):
    """Abstract factory for creating sessions (Factory Method Creator)."""
    @abstractmethod
    def create_session(self, time: str, room: str, teacher) -> ClassSession:
        """The factory method."""
        pass

class LectureFactory(SessionFactory):
    """Creates LectureSession objects."""
    def create_session(self, time: str, room: str, teacher) -> LectureSession:
        return LectureSession(time=time, room=room, teacher=teacher)

class PracticalFactory(SessionFactory):
    """Creates PracticalSession objects."""
    def create_session(self, time: str, room: str, teacher) -> PracticalSession:
        return PracticalSession(time=time, room=room, teacher=teacher)