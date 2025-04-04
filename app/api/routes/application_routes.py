from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.db.schema.application_schema import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationOut
)

from app.services.application_service import ApplicationService
from app.dependencies.application_dependencies import (
    get_application_service,
    get_valid_application
)
from app.core.security import get_current_user
from app.db.schema.user_schema import UserOut

router = APIRouter(prefix="/applications", tags=["applications"])

@router.post("/", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
async def create_application(
    application: ApplicationCreate,
    current_user: UserOut = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    return await service.create(application, str(current_user.id))

@router.get("/", response_model=List[ApplicationOut])
async def get_user_applications(
    skip: int = 0,
    limit: int = 10,
    current_user: UserOut = Depends(get_current_user),
    service: ApplicationService = Depends(get_application_service)
):
    return await service.get_by_user(str(current_user.id), skip, limit)

@router.get("/job/{job_id}", response_model=List[ApplicationOut])
async def get_job_applications(
    job_id: str,
    skip: int = 0,
    limit: int = 10,
    service: ApplicationService = Depends(get_application_service)
):
    return await service.get_by_job(job_id, skip, limit)

@router.get("/{application_id}", response_model=ApplicationOut)
async def get_application(
    application: ApplicationOut = Depends(get_valid_application)
):
    return application

@router.put("/{application_id}", response_model=ApplicationOut)
async def update_application(
    application_update: ApplicationUpdate,
    application: ApplicationOut = Depends(get_valid_application),
    service: ApplicationService = Depends(get_application_service)
):
    return await service.update(str(application.id), application_update)

@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(
    application: ApplicationOut = Depends(get_valid_application),
    service: ApplicationService = Depends(get_application_service)
):
    await service.delete(str(application.id))
    return None