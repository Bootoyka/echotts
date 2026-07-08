from datetime import datetime
from pydantic import BaseModel
from backend.app.jobs import JobStatus


class GenerateRequest(BaseModel):
    text: str
    voice: str = "default"


class GenerateResponse(BaseModel):
    job_id: str
    status: JobStatus


class JobResponse(BaseModel):
    job_id: str
    status: JobStatus
    audio_url: str | None = None
    created_at: datetime
    started_at: datetime | None = None
    completed_at: datetime | None = None
