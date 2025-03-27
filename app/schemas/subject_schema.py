from pydantic import BaseModel, Field
from typing import Optional

class SubjectBase(BaseModel): 
    code_name: str = Field(..., min_length=1, max_length=25)
    description: str
    difficulty: int = Field(..., ge=1, le=5)

class SubjectCreate(SubjectBase):
    pass

class SubjectRead(SubjectBase):
    id: int
    player_id: int

class SubjectUpdate(SubjectBase):
    code_name: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[int] = None