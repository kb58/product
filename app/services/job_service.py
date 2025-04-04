from typing import List, Optional
from app.db.model.job_model import Job, PyObjectId
from app.db.schema.job_schema import JobCreate, JobUpdate, JobOut
from interfaces import JobRepository
from datetime import datetime
from fastapi import HTTPException, status
from agents.description_analyzer import DescriptionAnalyzer

class JobService(JobRepository):
    def __init__(self):
        self.analyzer = DescriptionAnalyzer()

    async def create(self, job: JobCreate, recruiter_id: str) -> JobOut:
        # Analyze the description
        analyzed_desc, instructions = await self.analyzer.analyze_description(job.description)
        
        db_job = Job(
            **job.dict(),
            recruiter_id=PyObjectId(recruiter_id),
            analyzed_description=analyzed_desc,
            instructions=instructions
        )
        await db_job.save()
        return JobOut(**db_job.dict(by_alias=True))

    async def get_by_id(self, job_id: str) -> Optional[JobOut]:
        job = await Job.get(PyObjectId(job_id))
        if not job:
            return None
        return JobOut(**job.dict(by_alias=True))

    async def get_by_recruiter(self, recruiter_id: str, skip: int = 0, limit: int = 10) -> List[JobOut]:
        jobs = await Job.find(
            Job.recruiter_id == PyObjectId(recruiter_id)
        ).skip(skip).limit(limit).to_list()
        return [JobOut(**job.dict(by_alias=True)) for job in jobs]

    async def get_all(self, skip: int = 0, limit: int = 10, status: Optional[str] = None) -> List[JobOut]:
        query = Job.find()
        if status:
            query = query.find(Job.status == status)
        jobs = await query.skip(skip).limit(limit).to_list()
        return [JobOut(**job.dict(by_alias=True)) for job in jobs]

    async def update(self, job_id: str, job: JobUpdate) -> Optional[JobOut]:
        db_job = await Job.get(PyObjectId(job_id))
        if not db_job:
            return None
            
        update_data = job.dict(exclude_unset=True)
        
        # Re-analyze description if it's being updated
        if 'description' in update_data:
            analyzed_desc, instructions = await self.analyzer.analyze_description(update_data['description'])
            update_data['analyzed_description'] = analyzed_desc
            update_data['instructions'] = instructions
            
        update_data['updated_at'] = datetime.utcnow()
        
        await db_job.update({"$set": update_data})
        updated_job = await Job.get(PyObjectId(job_id))
        return JobOut(**updated_job.dict(by_alias=True))

    async def delete(self, job_id: str) -> bool:
        job = await Job.get(PyObjectId(job_id))
        if not job:
            return False
        await job.delete()
        return True

    async def search(self, query: str, skip: int = 0, limit: int = 10) -> List[JobOut]:
        jobs = await Job.find({
            "$text": {"$search": query}
        }).skip(skip).limit(limit).to_list()
        return [JobOut(**job.dict(by_alias=True)) for job in jobs]