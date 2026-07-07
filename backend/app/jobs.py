from dataclasses import dataclass
from enum import Enum
from pydantic import BaseModel

class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"

class Job(BaseModel):
    id: str
    text: str
    status: JobStatus
    audio_path: str | None = None