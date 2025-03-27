from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, String, ForeignKey, Integer, CheckConstraint

if TYPE_CHECKING:
    from app.models import Player, StudySession

class Subject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player_id: int = Field(sa_column=Column(ForeignKey("player.id", ondelete="CASCADE"), nullable=False))

    code_name: str = Field(sa_column=Column(String, nullable=False))
    description: str = Field(sa_column=Column(String, nullable=False))
    difficulty: int = Field(sa_column=Column(Integer, nullable=False), ge=1, le=5)

    player: "Player" = Relationship(back_populates="subjects")
    study_sessions: list["StudySession"] = Relationship(back_populates="subject")

    __table_args__ = (CheckConstraint("difficulty >= 1 AND difficulty <= 5", name="difficulty_range"),)
