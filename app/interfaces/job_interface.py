from typing import List, Optional
from app.db.schema.job_schema import JobCreate, JobUpdate, JobOut

class JobRepository:
    async def create(self, job: JobCreate, recruiter_id: str) -> JobOut:
        raise NotImplementedError

    async def get_by_id(self, job_id: str) -> Optional[JobOut]:
        raise NotImplementedError

    async def get_by_recruiter(self, recruiter_id: str, skip: int = 0, limit: int = 10) -> List[JobOut]:
        raise NotImplementedError

    async def get_all(self, skip: int = 0, limit: int = 10, status: Optional[str] = None) -> List[JobOut]:
        raise NotImplementedError

    async def update(self, job_id: str, job: JobUpdate) -> Optional[JobOut]:
        raise NotImplementedError

    async def delete(self, job_id: str) -> bool:
        raise NotImplementedError

    async def search(self, query: str, skip: int = 0, limit: int = 10) -> List[JobOut]:
        raise NotImplementedError