from pydantic import BaseModel
from typing import Optional

class PlayerCreate(BaseModel):
    id: int
    title: Optional[str] = "Noobie" 
    level: Optional[int] = 1
    experience: Optional[int] = 0

class PlayerRead(BaseModel):
    id: int
    username: str
    email: str
    title: str
    level: int
    experience: int
