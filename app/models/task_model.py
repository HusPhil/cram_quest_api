from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Column, ForeignKey, Relationship, DateTime, String
from datetime import datetime


if TYPE_CHECKING:
    from app.models import StudySession


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    study_session_id: int = Field(
        sa_column=Column(
            ForeignKey("studysession.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        )
    )

    description: str = Field(sa_column=Column(String, nullable=False))

    start_time: datetime = Field(
        default_factory=None, sa_type=DateTime(timezone=True), nullable=True
    )
    end_time: Optional[datetime] = Field(
        default=None, sa_type=DateTime(timezone=True), nullable=True
    )

    study_session: "StudySession" = Relationship(back_populates="tasks")
