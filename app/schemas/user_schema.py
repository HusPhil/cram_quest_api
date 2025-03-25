from typing import Annotated
from typing import Optional
from pydantic import EmailStr, SecretStr, Field, BaseModel

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, strip_whitespace=True)
    email: EmailStr

class UserRead(UserBase):
    id: int

class UserCreate(UserBase):
    password: SecretStr

class UserUpdate(BaseModel):  # ✅ Schema for updating users (all fields optional)
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[SecretStr] = None