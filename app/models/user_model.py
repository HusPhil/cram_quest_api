from typing import Optional, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship
from app.models.base import Base  # Inherit from Base

if TYPE_CHECKING:
    from app.models.player_model import Player  # Import only for type hints

class User(Base, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password: str = Field(nullable=False)

    player: Optional["Player"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"})
