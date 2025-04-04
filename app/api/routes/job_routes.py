from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from app.db.schema.job_schema import JobCreate, JobUpdate, JobOut
from app.services.job_service import JobService
from app.dependencies.job_dependencies import (
    get_job_service,
    get_valid_job,
    verify_recruiter
)
from app.core.security import get_current_user
from app.db.schema.user_schema import UserOut

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("/", response_model=JobOut, status_code=status.HTTP_201_CREATED)
async def create_job(
    job: JobCreate,
    current_user: UserOut = Depends(verify_recruiter),
    service: JobService = Depends(get_job_service)
):
    return await service.create(job, str(current_user.id))

@router.get("/", response_model=List[JobOut])
async def get_all_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: Optional[str] = Query(None),
    service: JobService = Depends(get_job_service)
):
    return await service.get_all(skip, limit, status)

@router.get("/search", response_model=List[JobOut])
async def search_jobs(
    query: str = Query(..., min_length=2),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    service: JobService = Depends(get_job_service)
):
    return await service.search(query, skip, limit)

@router.get("/my", response_model=List[JobOut])
async def get_my_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: UserOut = Depends(verify_recruiter),
    service: JobService = Depends(get_job_service)
):
    return await service.get_by_recruiter(str(current_user.id), skip, limit)

@router.get("/{job_id}", response_model=JobOut)
async def get_job(
    job: JobOut = Depends(get_valid_job)
):
    return job

@router.put("/{job_id}", response_model=JobOut)
async def update_job(
    job_update: JobUpdate,
    job: JobOut = Depends(get_valid_job),
    current_user: UserOut = Depends(verify_recruiter),
    service: JobService = Depends(get_job_service)
):
    if str(job.recruiter_id) != str(current_user.id) and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own jobs"
        )
    return await service.update(str(job.id), job_update)

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job: JobOut = Depends(get_valid_job),
    current_user: UserOut = Depends(verify_recruiter),
    service: JobService = Depends(get_job_service)
):
    if str(job.recruiter_id) != str(current_user.id) and current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own jobs"
        )
    await service.delete(str(job.id))
    return None