from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List
from bson import ObjectId
from enum import Enum

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class JobStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    CLOSED = "closed"

class Job(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    description: str = Field(...)
    analyzed_description: Optional[str] = None
    instructions: Optional[str] = None
    department: str = Field(...)
    openings: int = Field(..., gt=0)
    recruiter_id: PyObjectId = Field(...)
    status: JobStatus = Field(default=JobStatus.DRAFT)
    skills_required: List[str] = Field(default_factory=list)
    location: Optional[str] = None
    salary_range: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: Optional[datetime] = None

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "Senior Python Developer",
                "description": "We are looking for an experienced Python developer...",
                "department": "Engineering",
                "openings": 3,
                "recruiter_id": "507f1f77bcf86cd799439011",
                "skills_required": ["Python", "FastAPI", "MongoDB"],
                "location": "Remote",
                "salary_range": "$90,000 - $120,000"
            }
        }