from abc import ABC, abstractmethod
from typing import List, Tuple
from .sessions import ClassSession, ProgrammingLecture, ProgrammingPractical
from .courseworks import CourseWork, ProgrammingCourseWork
from .teachers import Teacher

class CourseFactory(ABC):
    """
    Abstract Factory for creating a family of related products (sessions, coursework).
    This ensures consistency across course components.
    """
    
    @abstractmethod
    def create_lecture(self, time: str, room: str, teacher: Teacher) -> ClassSession:
        pass

    @abstractmethod
    def create_practical(self, time: str, room: str, teacher: Teacher) -> ClassSession:
        pass

    @abstractmethod
    def create_coursework(self, mentor: Teacher) -> CourseWork:
        pass
    
    def create_full_course(self, lecture_params: Tuple, practical_params: Tuple, mentor: Teacher) -> Tuple[List[ClassSession], CourseWork]:
        """Utility method to create a full consistent course package."""
        lecture = self.create_lecture(*lecture_params)
        practical = self.create_practical(*practical_params)
        coursework = self.create_coursework(mentor)
        return [lecture, practical], coursework


class ProgrammingCourseFactory(CourseFactory):
    """Creates a consistent set of objects for a Programming Course."""

    def create_lecture(self, time: str, room: str, teacher: Teacher) -> ProgrammingLecture:
        return ProgrammingLecture(time=time, room=room, teacher=teacher)

    def create_practical(self, time: str, room: str, teacher: Teacher) -> ProgrammingPractical:
        return ProgrammingPractical(time=time, room=room, teacher=teacher)

    def create_coursework(self, mentor: Teacher) -> ProgrammingCourseWork:
        return ProgrammingCourseWork(supervisor=mentor)