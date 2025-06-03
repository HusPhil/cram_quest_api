from pydantic import BaseModel
from typing import Optional
from enum import Enum


class MaterialType(str, Enum):
    VIDEO = "Video"
    FLASHCARD = "Flashcard"
    NOTE = "Note"


class MaterialBase(BaseModel):
    title: str
    type: MaterialType
    link: str


class MaterialCreate(MaterialBase):
    pass


class MaterialUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[MaterialType] = None
    link: Optional[str] = None


class MaterialRead(MaterialBase):
    id: int
    subject_id: int

    class Config:
        orm_mode = True
