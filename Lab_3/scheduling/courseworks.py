from abc import ABC, abstractmethod
from .teachers import ExternalMentor, Teacher

class CourseWork(ABC):
    """Abstract CourseWork Product."""
    def __init__(self, supervisor: ExternalMentor):
        if not isinstance(supervisor, ExternalMentor):
            raise ValueError("CourseWork must be supervised by an ExternalMentor.")
        self.supervisor = supervisor

    @abstractmethod
    def submission_format(self) -> str:
        pass

class ProgrammingCourseWork(CourseWork):
    """Concrete CourseWork Product for programming."""
    def submission_format(self) -> str:
        return "GitHub repository upload"