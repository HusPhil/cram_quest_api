from typing import Optional, TYPE_CHECKING
from enum import Enum
from sqlmodel import SQLModel, Field, Column, ForeignKey, Relationship, DateTime
from datetime import datetime, timezone

if TYPE_CHECKING:
    from app.models import Player, Subject

class SessionStatus(Enum):
    ACTIVE = "active"
    PENDING = "pending"
    COMPLETED = "completed"

class StudySession(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player_id: int = Field(
        sa_column=Column(ForeignKey("player.id", ondelete="CASCADE"), nullable=False)
    )
    subject_id: int = Field(
        sa_column=Column(ForeignKey("subject.id", ondelete="CASCADE"), nullable=False)
    )
    start_time: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True)
    )
    end_time: Optional[datetime] = Field(default=None, sa_type=DateTime(timezone=True))
    status: SessionStatus = Field(default=SessionStatus.ACTIVE)
    xp_earned: int = Field(default=0)

    player: "Player" = Relationship(back_populates="study_sessions")
    subject: "Subject" = Relationship(back_populates="study_sessions")