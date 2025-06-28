from pydantic import BaseModel, Field
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from app.models.study_session_model import SessionStatus
from app.schemas.task_schema import TaskRead


class StudySessionCreate(BaseModel):
    """Schema for creating a study session."""

    player_id: int
    quest_id: int
    subject_id: int
    duration_mins: int = Field(..., gt=0)
    tasks_to_create: list[str]


class StudySessionRead(BaseModel):
    """Schema for returning study session details."""

    id: int
    player_id: int
    quest_id: int
    subject_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    actual_complete_time: Optional[datetime] = None
    xp_earned: int
    status: SessionStatus
    tasks: list[TaskRead]
