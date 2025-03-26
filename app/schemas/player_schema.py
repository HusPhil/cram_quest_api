from pydantic import BaseModel
from app.models.player_model import PlayerTitle
from typing import Optional

class PlayerBase(BaseModel):
    title: PlayerTitle 
    level: int 
    experience:int

class PlayerCreate(BaseModel):
    title: Optional[PlayerTitle] = PlayerTitle.NOVICE 
    level: Optional[int] = 1
    experience: Optional[int] = 0

class PlayerRead(PlayerBase):
    id: int
    username: str
    email: str


