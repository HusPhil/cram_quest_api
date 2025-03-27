from datetime import datetime, timezone
from app.models.study_session_model import SessionStatus
from app.models import Player, StudySession
from sqlmodel import Session

class GameService:
    BASE_XP = 100  # Minimum XP needed for level-up
    INCREMENT = 50  # Small bonus per level
    MULTIPLIER = 20  # Controls exponential growth
    COMPLETION_BONUS = 30  # Extra XP for completing a session

    @staticmethod
    def calculate_xp(study_session: StudySession) -> int:
        """Calculate XP based on session duration, difficulty, and completion speed."""
        
        if not study_session.end_time:
            study_session.end_time = datetime.now(timezone.utc)

        # Duration calculations
        duration_minutes = (study_session.end_time - study_session.start_time).total_seconds() / 60
        expected_duration_minutes = study_session.expected_duration  # Store expected duration in model

        # Efficiency bonus (finishing early)
        efficiency_bonus = max(0, (expected_duration_minutes / duration_minutes) * 10) if duration_minutes > 0 else 0

        # Difficulty bonus
        difficulty_bonus = study_session.subject.difficulty * 5

        # Completion bonus
        completion_bonus = GameService.COMPLETION_BONUS if study_session.status == SessionStatus.COMPLETED else 0

        # XP formula
        xp_earned = int(GameService.BASE_XP + (duration_minutes / 15 * GameService.BASE_XP) + difficulty_bonus + completion_bonus + efficiency_bonus)

        return max(xp_earned, 0)  # Ensure XP is never negative

    @staticmethod
    def next_level_xp(level: int) -> int:
        """Calculate XP required to reach the next level."""
        return int(GameService.BASE_XP + (level * GameService.INCREMENT) + (level ** 1.5 * GameService.MULTIPLIER))
