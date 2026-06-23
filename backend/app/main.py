import uuid
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.app.jobs import Job, JobStatus
from backend.app.queue import job_queue
from backend.app.schemas import GenerateResponse, GenerateRequest
from backend.app.tts import generate_audio
from backend.app.store import load_jobs, save_jobs
from backend.app.logger import logger

jobs = load_jobs()


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(worker())
    yield
app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate", response_model=GenerateResponse)
async def generate(payload: GenerateRequest):
    job_id = str(uuid.uuid4())

    job = Job(
        id=job_id,
        text=payload.text,
        status= JobStatus.QUEUED
    )

    jobs[job_id] = job
    save_jobs(jobs)

    await job_queue.put(job_id)

    return GenerateResponse(
        job_id=job_id,
        status=job.status.value
    )

@app.get("/status/{job_id}")
def get_status(job_id: str):
    job = jobs.get(job_id)

    if not job:
        return {"error": "job not found"}

    return {
        "job_id": job.id,
        "status": job.status.value,
        "audio_path": job.audio_path
    }

async def worker():
    while True:
        job_id = await job_queue.get()
        job = jobs.get(job_id)

        if not job:
            job_queue.task_done()
            continue

        try:
            path = generate_audio(job.text, job.id)
            job.status = JobStatus.DONE
            job.audio_path = path

        except Exception as e:
            job.status = JobStatus.FAILED
            logger.exception("Job failed: %s", job.id)

        save_jobs(jobs)
        job_queue.task_done()
