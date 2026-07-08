from datetime import datetime, timezone
from enum import Enum
from pydantic import BaseModel, Field


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
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    started_at: datetime | None = None
    completed_at: datetime | None = None

@property
def processing_time(self):
    if not self.started_at or not self.completed_at:
        return None
    return (self.completed_at - self.started_at).total_seconds()