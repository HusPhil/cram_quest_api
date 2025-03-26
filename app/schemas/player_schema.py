from pydantic import BaseModel, Field
from app.models.player_model import PlayerTitle
from typing import Optional

class PlayerBase(BaseModel):
    title: PlayerTitle 
    level: int 
    experience:int

class PlayerCreate(BaseModel):
    title: PlayerTitle = Field(default=PlayerTitle.NOVICE, description="Choose a player title")
    level: Optional[int] = 1
    experience: Optional[int] = 0

class PlayerRead(PlayerBase):
    id: int
    username: str
    email: str


