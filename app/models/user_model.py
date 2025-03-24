from typing import Optional
from sqlmodel import Field
from app.models.base import Base  # Inherit from Base

class User(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    password: str
