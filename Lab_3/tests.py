import pytest
from scheduling.courses import ProgrammingCourseFactory
from scheduling.teachers import Lecturer, Assistant, ExternalMentor
from scheduling.groups import StudentGroup
from scheduling.factories import LectureFactory, PracticalFactory
from scheduling.sessions import LectureSession, PracticalSession

def test_group_enrollment_and_conflict_detection():
    """Tests the Abstract Factory integration and the conflict detection logic."""
    
    course_factory = ProgrammingCourseFactory()
    
    lecturer = Lecturer("Oleh Sinkevych")
    assistant = Assistant("Dr. Mariia Petrenko")
    mentor = ExternalMentor("Industry Expert")

    lecture = course_factory.create_lecture(
        time="Wed 15:05", room="129", teacher=lecturer
    )
    practical = course_factory.create_practical(
        time="Mon 13:30", room="#3", teacher=assistant
    )
    coursework = course_factory.create_coursework(mentor=mentor)

    practical_conflict = course_factory.create_practical(
        time="Mon 13:30", room="#5", teacher=assistant
    )

    group = StudentGroup("FeP-23")
    group.add_session(lecture)
    group.add_session(practical)
    group.add_session(practical_conflict)

    conflicts = group.check_conflicts()
    
    assert len(conflicts) == 1
    
    session_a, session_b = conflicts[0]
    assert session_a.time == "Mon 13:30"
    assert session_b.time == "Mon 13:30"
    
    assert coursework.supervisor == mentor

def test_lecture_factory_creates_lecture():
    """Tests the Factory Method for creating lectures."""
    factory = LectureFactory()
    teacher = Lecturer("Oleh Sinkevych")
    session = factory.create_session(time="Wed 15:05", room="129", teacher=teacher)
    
    assert isinstance(session, LectureSession)
    assert session.teacher == teacher

def test_teacher_restriction():
    """Tests the validation logic for teacher compatibility (SOLID)."""
    factory = LectureFactory()
    mentor = ExternalMentor("Industry Expert")
    
    with pytest.raises(ValueError) as excinfo:
        factory.create_session(time="Wed 10:00", room="101", teacher=mentor)
    assert "cannot teach a Lecture" in str(excinfo.value)