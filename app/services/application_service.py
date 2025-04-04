from typing import List, Optional
from app.db.model.application_model import Application, PyObjectId
from app.db.schema.application_schema import ApplicationCreate, ApplicationUpdate, ApplicationOut
from app.interfaces.application_interface import ApplicationRepository
from datetime import datetime
from fastapi import HTTPException, status

class ApplicationService(ApplicationRepository):
    async def create(self, application: ApplicationCreate, user_id: str) -> ApplicationOut:
        db_application = Application(
            user_id=PyObjectId(user_id),
            job_id=PyObjectId(application.job_id),
            resume_id=PyObjectId(application.resume_id),
            notes=application.notes
        )
        await db_application.save()
        return ApplicationOut(**db_application.dict(by_alias=True))

    async def get_by_id(self, application_id: str) -> Optional[ApplicationOut]:
        application = await Application.get(PyObjectId(application_id))
        if not application:
            return None
        return ApplicationOut(**application.dict(by_alias=True))

    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 10) -> List[ApplicationOut]:
        applications = await Application.find(
            Application.user_id == PyObjectId(user_id)
        ).skip(skip).limit(limit).to_list()
        return [ApplicationOut(**app.dict(by_alias=True)) for app in applications]

    async def get_by_job(self, job_id: str, skip: int = 0, limit: int = 10) -> List[ApplicationOut]:
        applications = await Application.find(
            Application.job_id == PyObjectId(job_id)
        ).skip(skip).limit(limit).to_list()
        return [ApplicationOut(**app.dict(by_alias=True)) for app in applications]

    async def update(self, application_id: str, application: ApplicationUpdate) -> Optional[ApplicationOut]:
        db_application = await Application.get(PyObjectId(application_id))
        if not db_application:
            return None
            
        update_data = application.dict(exclude_unset=True)
        update_data['updated_at'] = datetime.utcnow()
        
        await db_application.update({"$set": update_data})
        updated_application = await Application.get(PyObjectId(application_id))
        return ApplicationOut(**updated_application.dict(by_alias=True))

    async def delete(self, application_id: str) -> bool:
        application = await Application.get(PyObjectId(application_id))
        if not application:
            return False
        await application.delete()
        return True