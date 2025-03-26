from pydantic import BaseModel, Field
from app.models.player_model import PlayerTitle
from app.models.profile_model import Mood
from typing import Optional

class Profile(BaseModel):
    avatar_url: PlayerTitle 
    level: int 
    experience:int

class ProfileCreate(BaseModel):
    avatar_url: str = "default.png"
    bio: str = ""
    mood: Mood = Mood.NEUTRAL