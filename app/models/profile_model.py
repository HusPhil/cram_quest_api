from typing import Optional, TYPE_CHECKING
from enum import Enum
from sqlmodel import SQLModel, Field, Column, ForeignKey, String, Relationship

if TYPE_CHECKING:
    from app.models import Player


class Mood(str, Enum):
    HAPPY = "Happy"
    MOTIVATED = "Motivated"
    NEUTRAL = "Neutral"
    STRESSED = "Stressed"
    EXHAUSTED = "Exhausted"

class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    player_id: int = Field(sa_column=Column(ForeignKey("player.id", ondelete="CASCADE"), unique=True, nullable=False))

    avatar_url: Optional[str] = Field(default="default/default_1.png")  
    bio: Optional[str] = Field(default="")  
    mood: Mood = Field(sa_column=Column(String, nullable=False), default=Mood.NEUTRAL)  

    player: "Player" = Relationship(back_populates="profile")