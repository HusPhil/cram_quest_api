from pydantic import BaseModel, Field, EmailStr
from app.models.player_model import PlayerTitle
from app.models.profile_model import Mood
from typing import Optional


class SignUpRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=12, strip_whitespace=True)
    email: EmailStr
    password: str = Field(..., min_length=8)
    avatar_url: Optional[str] = Field(default=None)

class UserInfo(BaseModel):
    id: int
    username: str
    email: EmailStr

class PlayerInfo(BaseModel):
    id: int

class ProfileInfo(BaseModel):
    id: int
    avatar_url: Optional[str]

class AuthenticationResponse(BaseModel):
    user_info: UserInfo
    player: PlayerInfo
    profile: ProfileInfo
    access_token: str
