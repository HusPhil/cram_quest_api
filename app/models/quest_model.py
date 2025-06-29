from typing import Optional, TYPE_CHECKING
from enum import Enum
from sqlmodel import (
    SQLModel,
    Field,
    Column,
    ForeignKey,
    Relationship,
    DateTime,
    String,
    Integer,
)
from datetime import datetime, timezone


if TYPE_CHECKING:
    from app.models import Subject, StudySession


class QuestStatus(str, Enum):  # Ensure it stores properly in DB
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Quest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    subject_id: int = Field(
        sa_column=Column(
            ForeignKey("subject.id", ondelete="CASCADE"), nullable=False, index=True
        )
    )

    description: str = Field(sa_column=Column(String, nullable=False))
    difficulty: int = Field(sa_column=Column(Integer, nullable=False), ge=1, le=5)

    status: QuestStatus = Field(
        sa_column=Column(String, nullable=False), default=QuestStatus.IN_PROGRESS
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),
    )

    subject: "Subject" = Relationship(back_populates="quests")
    study_sessions: Optional["StudySession"] = Relationship(back_populates="quest")
