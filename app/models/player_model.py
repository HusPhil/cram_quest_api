from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship, Column, String, ForeignKey
from enum import Enum


if TYPE_CHECKING:
    from app.models.user_model import User  # ✅ Type Hint Only
    from app.models.profile_model import Profile
    from app.models.subject_model import Subject

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
    user_id: int = Field(
        sa_column=Column(ForeignKey("user.id", ondelete="CASCADE"), nullable=False, unique=True, index=True)
    )
    title: PlayerTitle = Field(
        sa_column=Column(String, nullable=False), default=PlayerTitle.NOVICE 
    )
    level: int = Field(default=1)  
    experience: int = Field(default=0)

    user: "User" = Relationship(back_populates="player") 
    profile: Optional["Profile"] = Relationship(back_populates="player", sa_relationship_kwargs={"cascade": "all, delete"})  
    subjects: list["Subject"] = Relationship(back_populates="player", sa_relationship_kwargs={"cascade": "all, delete"})
    
