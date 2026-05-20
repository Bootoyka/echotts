from dataclasses import dataclass
from typing import Optional

@dataclass
class Job:
    id: str
    text: str
    status: str = "queued"
    audio_path: Optional[str] = None