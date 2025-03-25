from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from app.models.base import Base  # Inherit from Base

if TYPE_CHECKING:
    from app.models.player_model import Player 

class User(Base, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)  # ✅ Ensure unique usernames
    email: str = Field(unique=True, index=True)  # ✅ Prevent duplicate emails
    password: str = Field(nullable=False)  # ✅ Ensure password is required

    player: Optional["Player"] = Relationship(back_populates="user")
