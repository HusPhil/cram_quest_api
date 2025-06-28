from typing import Optional
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field



class TaskBase(BaseModel):
    study_session_id: int
    description: str = Field(None, min_length=1, max_length=255)
    
class TaskCreate(TaskBase):
    pass

class TaskRead(TaskBase):
    id: int
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

class TaskStart(BaseModel):
    id: int
    start_time: datetime

class TaskEnd(BaseModel):
    id: int
    end_time: datetime

