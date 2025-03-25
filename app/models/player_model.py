from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, String
from enum import Enum


if TYPE_CHECKING:
    from app.models.user_model import User  # ✅ Import only for type hints

class PlayerTitle(str, Enum):
    NOVICE = "Novice"
    APPRENTICE = "Apprentice"
    ADEPT = "Adept"
    SCHOLAR = "Scholar"
    SAGE = "Sage"
    ARCHMAGE = "Archmage"
    OMNISCIENT = "Omniscient"

class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", unique=True)
    title: int = Field(default=1)
    level: PlayerTitle = Field(sa_column=Column(String, nullable=False))
    experience: int = Field(default=0)

    user: "User" = Relationship(back_populates="player")  # ✅ Ensures bidirectional link
