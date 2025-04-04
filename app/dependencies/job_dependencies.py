from fastapi import Depends, HTTPException, status
from typing import Annotated
from app.services.job_service import JobService
from app.core.security import get_current_user
from app.db.schema.user_schema import UserOut, UserRole

def get_job_service() -> JobService:
    return JobService()

async def get_valid_job(
    job_id: str,
    service: JobService = Depends(get_job_service)
):
    job = await service.get_by_id(job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return job

async def verify_recruiter(user: UserOut = Depends(get_current_user)):
    if user.role != UserRole.RECRUITER and user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only recruiters can perform this action"
        )
    return user