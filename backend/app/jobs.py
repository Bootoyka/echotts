from dataclasses import dataclass
from enum import Enum
from typing import Optional

class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"

@dataclass
class Job:
    id: str
    text: str
    status: JobStatus = JobStatus.QUEUED
    audio_path: Optional[str] = None