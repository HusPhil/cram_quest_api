from sqlmodel import SQLModel, Field
from app.models.user_model import User

class Player(SQLModel, table=True):
    id: int = Field(primary_key=True, foreign_key="user.id")  # Links to User ID
    title: str = Field(default="Noobie")
    level: int = Field(default=1)
    experience: int = Field(default=0)
    
