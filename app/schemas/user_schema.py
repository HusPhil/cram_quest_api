from typing import Annotated
from pydantic import BaseModel, EmailStr, SecretStr, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, strip_whitespace=True)
    email: EmailStr
    password: SecretStr

class UserRead(BaseModel):
    id: int
    username: str
    email: str

# class UserUpdate(BaseModel):
#     username: Annotated[str, Field(..., min_length=3, strip_whitespace=True)]   
#     email: EmailStr
#     password: SecretStr