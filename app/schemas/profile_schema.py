from pydantic import BaseModel, Field
from app.models.player_model import PlayerTitle
from app.models.profile_model import Mood
from typing import Optional


class ProfileCreate(BaseModel):
    avatar_url: str = "default/default_1.png"
    bio: str = ""
    mood: Mood = Mood.NEUTRAL

class ProfileBase(BaseModel):
    avatar_url: Optional[str] 
    bio: Optional[str]
    mood: Optional[Mood]

class ProfileRead(ProfileBase):
    id: int
    player_id: int

class ProfileUpdate(BaseModel):
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    mood: Optional[Mood] = None 