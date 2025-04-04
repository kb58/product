from fastapi import Depends, HTTPException, status
from typing import Annotated
from app.services.application_service import ApplicationService

def get_application_service() -> ApplicationService:
    return ApplicationService()

async def get_valid_application(
    application_id: str,
    service: ApplicationService = Depends(get_application_service)
):
    application = await service.get_by_id(application_id)
    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )
    return application