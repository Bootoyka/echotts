from backend.app.jobs import Job
from backend.app.database import get_db

def _get_jobs_collection():
    db = get_db()

    return db["jobs"]

async def save_job(job: Job):
    collection = _get_jobs_collection()
    job_data = job.model_dump()

    await collection.update_one(
        {"id": job.id},
        {"$set": job_data},
        upsert=True
    )
    print(f"Job {job.id} saved")

async def  get_job(job_id: str) -> Job | None:
    collection = _get_jobs_collection()
    job_data = await collection.find_one({"id": job_id})

    if not job_data:
        return None
    return Job(**job_data)

async def delete_job(job_id: str) -> bool:
    collection = _get_jobs_collection()
    result = await collection.delete_one({"id": job_id})

    return result.deleted_count > 0

async def clean_database() -> None:
    collection = _get_jobs_collection()
    await collection.delete_many({})

