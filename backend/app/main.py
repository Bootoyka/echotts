import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from backend.app.database import init_database, close_database
from backend.app.jobs import Job, JobStatus
from backend.app.queue import enqueue
from backend.app.schemas import GenerateResponse, GenerateRequest, JobResponse
from backend.app import jobs_crud


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Atlas MongoDB connection...")
    db_client = init_database()

    try:
        await db_client.admin.command("ping")
        print("connection successful")
    except Exception as e:
        print(f"connection failed : {e}")
        raise e

    yield

    close_database()
    print("Atlas Mongodb connection closed")
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
        status= JobStatus.QUEUED,
    )

    await jobs_crud.save_job(job)
    enqueue(job_id)

    return GenerateResponse(
        job_id=job_id,
        status=job.status
    )

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    job = await jobs_crud.get_job(job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    return JobResponse(
        job_id=job_id,
        status=job.status,
        audio_url=f"audio/{job_id}" if job.audio_path else None,
        created_at=job.created_at,
        started_at=job.started_at,
        completed_at=job.completed_at
        )

@app.get("/audio/{job_id}")
async def get_audio(job_id: str):
    job = await jobs_crud.get_job(job_id)

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    if not job.audio_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )

    audio_file = Path(job.audio_path)

    if not audio_file.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audio file not found"
        )

    return FileResponse(
        path=audio_file,
        media_type="audio/wav",
        filename=f"{job.id}.wav",
    )