from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, String, ForeignKey, Integer

if TYPE_CHECKING:
    from app.models.player_model import Player
    from app.models.study_session_model import StudySession
    from app.models.quest_model import Quest
    from app.models.material_model import Material


class Subject(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player_id: int = Field(sa_column=Column(ForeignKey("player.id", ondelete="CASCADE"), nullable=False))

    code_name: str = Field(sa_column=Column(String, nullable=False))
    description: str = Field(sa_column=Column(String, nullable=False))
    difficulty: int = Field(sa_column=Column(Integer, nullable=False), ge=1, le=5)

    player: Optional["Player"] = Relationship(back_populates="subjects")
    study_sessions: List["StudySession"] = Relationship(back_populates="subject")
    quests: List["Quest"] = Relationship(back_populates="subject", sa_relationship_kwargs={"cascade": "all, delete"})
    materials: list["Material"] = Relationship(back_populates="subject", sa_relationship_kwargs={"cascade": "all, delete"})
