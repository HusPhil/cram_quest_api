from sqlmodel import Field
from app.models.base import Base  # Inherit from Base

class User(Base, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
