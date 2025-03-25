from sqlmodel import SQLModel, Field
from typing import Optional, TYPE_CHECKING
from sqlmodel import Relationship


if TYPE_CHECKING:
    from app.models.user_model import User

class Player(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)  # ✅ Auto-incrementing ID
    user_id: int = Field(foreign_key="user.id", unique=True)  # ✅ Ensures 1:1 User-Player
    title: str = Field(default="Noobie")
    level: int = Field(default=1)
    experience: int = Field(default=0)

    user: "User" = Relationship(back_populates="player")
    
