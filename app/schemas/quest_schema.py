from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class QuestStatus(str, Enum):
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class QuestBase(BaseModel):
    subject_id: int
    description: str 
    difficulty: int = Field(..., ge=1, le=5, description="Difficulty level (1 to 5)")
    status: QuestStatus = QuestStatus.IN_PROGRESS

class QuestCreate(BaseModel):
    subject_id: int
    description: str 
    difficulty: int = Field(..., ge=1, le=5, description="Difficulty level (1 to 5)")

class QuestRead(QuestBase):
    id: int
    created_at: datetime

class QuestUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=5, max_length=255)
    difficulty: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[QuestStatus] = None