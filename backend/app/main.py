from fastapi import FastAPI
from backend.app.models import Job
import uuid
from backend.app.queue import job_queue
import asyncio
from backend.app.tts import generate_audio

app = FastAPI()

jobs = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/generate")
async def generate(payload: dict):
    job_id = str(uuid.uuid4())

    job = Job(
        id=job_id,
        text=payload["text"],
        status="queued"
    )

    jobs[job_id] = job

    await job_queue.put(job_id)

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

async def worker():
    while True:
        job_id = await job_queue.get()
        job = jobs.get(job_id)

        if not job:
            job_queue.task_done()
            continue

        # transition state
        job.status = "processing"

        path = generate_audio(job.text, job.id)

        print("JOB_ID:", job.id)
        print("TEXT:", repr(job.text))
        print("OUTPUT:", path)

        job.status = "done"
        job.audio_path = path

        job_queue.task_done()

@app.on_event("startup")
async def startup():
    asyncio.create_task(worker())