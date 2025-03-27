from pydantic import BaseModel, Field
from app.models.player_model import PlayerTitle
from app.models.profile_model import Mood
from typing import Optional
from datetime import datetime
from app.models.study_session_model import SessionStatus


class StudySessionCreate(BaseModel):
    """Schema for creating a study session."""
    player_id: int
    subject_id: int
    duration_mins: int = Field(..., gt=0)

class StudySessionRead(BaseModel):
    """Schema for returning study session details."""
    id: int
    player_id: int
    subject_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    xp_earned: int
    status: SessionStatus

