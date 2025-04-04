from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    REVIEWED = "reviewed"
    INTERVIEW = "interview"
    REJECTED = "rejected"
    OFFERED = "offered"

class ApplicationCreate(BaseModel):
    job_id: str = Field(...)
    resume_id: str = Field(...)
    notes: Optional[str] = None

class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None
    notes: Optional[str] = None

class ApplicationOut(BaseModel):
    id: str
    user_id: int
    job_id: str
    resume_id: str
    status: ApplicationStatus
    applied_at: datetime
    updated_at: datetime
    notes: Optional[str] = None

    class Config:
        orm_mode = True