from typing import List, Tuple
from .sessions import ClassSession

class StudentGroup:
    """
    Represents a student group and manages its schedule (Composition).
    Its primary responsibility is conflict detection (SRP).
    """
    def __init__(self, name: str):
        self.name = name
        self._schedule: List[ClassSession] = []

    def enroll_course(self, sessions: List[ClassSession]):
        """Enrolls the group in a course by adding all sessions."""
        for session in sessions:
            self.add_session(session)

    def add_session(self, session: ClassSession):
        """Adds a single session to the schedule."""
        self._schedule.append(session)

    def check_conflicts(self) -> List[Tuple[ClassSession, ClassSession]]:
        """Detects scheduling conflicts (two sessions at the same time)."""
        conflicts = []
        n = len(self._schedule)
        for i in range(n):
            for j in range(i + 1, n):
                session1 = self._schedule[i]
                session2 = self._schedule[j]

                if session1.time == session2.time:
                    conflicts.append((session1, session2))

        return conflicts
    
    def __repr__(self):
        return f"StudentGroup('{self.name}', sessions={len(self._schedule)})"