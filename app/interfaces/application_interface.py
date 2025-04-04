from typing import List, Optional
from app.db.model.application_model import Application
from app.db.schema.application_schema import ApplicationCreate, ApplicationUpdate, ApplicationOut

class ApplicationRepository:
    async def create(self, application: ApplicationCreate, user_id: str) -> ApplicationOut:
        raise NotImplementedError

    async def get_by_id(self, application_id: str) -> Optional[ApplicationOut]:
        raise NotImplementedError

    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 10) -> List[ApplicationOut]:
        raise NotImplementedError

    async def get_by_job(self, job_id: str, skip: int = 0, limit: int = 10) -> List[ApplicationOut]:
        raise NotImplementedError

    async def update(self, application_id: str, application: ApplicationUpdate) -> Optional[ApplicationOut]:
        raise NotImplementedError

    async def delete(self, application_id: str) -> bool:
        raise NotImplementedError