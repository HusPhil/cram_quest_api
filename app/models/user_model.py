from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, Relationship
from app.models.base import Base

if TYPE_CHECKING:
    from app.models import Player
    
class User(Base, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password: str = Field(nullable=False)
    is_active: bool = Field(default=False)
    is_admin: bool = Field(default=False)

    player: Optional["Player"] = Relationship(back_populates="user", sa_relationship_kwargs={"cascade": "all, delete"})
