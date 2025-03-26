from pydantic import BaseModel, Field
from app.models.player_model import PlayerTitle
from app.models.profile_model import Mood
from typing import Optional

class ProfileBase(BaseModel):
    avatar_url: str 
    bio: str
    mood: str

class ProfileCreate(BaseModel):
    avatar_url: str = "default.png"
    bio: str = ""
    mood: Mood = Mood.NEUTRAL

class ProfileRead(ProfileBase):
    id: int
    player_id: int
