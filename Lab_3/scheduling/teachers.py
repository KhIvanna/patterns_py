from abc import ABC, abstractmethod

class Teacher(ABC):
    """
    Abstract Teacher. Adheres to the Liskov Substitution Principle (LSP)
    by implementing a method to check capability.
    """
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}')"

    @abstractmethod
    def can_teach(self, session_type: str) -> bool:
        """Checks if the teacher can lead a specific session type."""
        pass

class Lecturer(Teacher):
    """Lecturer - can teach lectures."""
    def can_teach(self, session_type: str) -> bool:
        return session_type == "Lecture"

class Assistant(Teacher):
    """Assistant - can lead practical sessions."""
    def can_teach(self, session_type: str) -> bool:
        return session_type == "Practical"

class ExternalMentor(Teacher):
    """
    External Mentor - cannot teach sessions but can supervise coursework.
    This separation adheres to Interface Segregation Principle (ISP) if extended.
    """
    def can_teach(self, session_type: str) -> bool:
        return False
    
    def can_supervise_coursework(self) -> bool:
        """Specific capability for CourseWork supervision."""
        return True