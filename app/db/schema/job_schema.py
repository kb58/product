from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum

class JobStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"

class JobCreate(BaseModel):
    title: str = Field(..., min_length=5, max_length=100)
    description: str = Field(..., min_length=20)
    department: str = Field(..., min_length=2, max_length=50)
    openings: int = Field(..., gt=0)
    skills_required: List[str] = Field(default_factory=list)
    location: Optional[str] = Field(None, max_length=100)
    salary_range: Optional[str] = Field(None, max_length=50)

class JobUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=100)
    description: Optional[str] = Field(None, min_length=20)
    department: Optional[str] = Field(None, min_length=2, max_length=50)
    openings: Optional[int] = Field(None, gt=0)
    status: Optional[JobStatus] = None
    skills_required: Optional[List[str]] = None
    location: Optional[str] = Field(None, max_length=100)
    salary_range: Optional[str] = Field(None, max_length=50)
    expires_at: Optional[datetime] = None

class JobOut(BaseModel):
    id: str
    title: str
    description: str
    analyzed_description: Optional[str]
    instructions: Optional[str]
    department: str
    openings: int
    recruiter_id: str
    status: JobStatus
    skills_required: List[str]
    location: Optional[str]
    salary_range: Optional[str]
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime]

    class Config:
        orm_mode = True