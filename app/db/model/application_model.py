from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
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
    def  __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")

class ApplicationStatus(str, Enum):
    APPLIED = "applied"
    REVIEWED = "reviewed"
    INTERVIEW = "interview"
    REJECTED = "rejected"
    OFFERED = "offered"

class Application(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    user_id: PyObjectId = Field(...)
    job_id: PyObjectId = Field(...)
    resume_id: PyObjectId = Field(...)
    status: ApplicationStatus = Field(default=ApplicationStatus.APPLIED)
    applied_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None

    class Config:
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "job_id": "507f1f77bcf86cd799439012",
                "resume_id": "507f1f77bcf86cd799439013",
                "status": "applied",
                "notes": "Highly qualified candidate"
            }
        }