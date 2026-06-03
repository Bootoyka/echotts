from pydantic import BaseModel


class GenerateRequest(BaseModel):
    text: str
    voice: str = "default"


class GenerateResponse(BaseModel):
    job_id: str
    status: str


class StatusResponse(BaseModel):
    job_id: str
    status: str
    audio_path: str | None = None