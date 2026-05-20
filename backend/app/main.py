from fastapi import FastAPI
from backend.app.models import Job
import uuid

app = FastAPI()

jobs = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate")
def generate(payload: dict):
    job_id = str(uuid.uuid4())

    job = Job(
        id=job_id,
        text=payload["text"],
        status="queued"
    )

    jobs[job_id] = job

    return {
        "job_id": job_id,
        "status": job.status
    }

@app.get("/status/{job_id}")
def get_status(job_id: str):
    job = jobs.get(job_id)

    if not job:
        return {"error": "job not found"}

    return {
        "job_id": job.id,
        "status": job.status,
        "audio_path": job.audio_path
    }