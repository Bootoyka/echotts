from backend.app.jobs import Job
from backend.app.worker_database import get_worker_db


def _get_jobs_collection():
    db = get_worker_db()
    return db["jobs"]


def get_job(job_id: str) -> Job | None:
    collection = _get_jobs_collection()

    job_data = collection.find_one({"id": job_id})

    if not job_data:
        return None

    return Job(**job_data)


def save_job(job: Job):
    collection = _get_jobs_collection()

    collection.update_one(
        {"id": job.id},
        {"$set": job.model_dump()},
        upsert=True
    )

    print(f"Worker saved job {job.id}: {job.status}")