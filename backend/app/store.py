import json
from pathlib import Path
from backend.app.models import Job, JobStatus

DB_PATH = Path("data/jobs.json")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def load_jobs() -> dict:
    if not DB_PATH.exists():
        return {}

    with open(DB_PATH, "r") as f:
        raw = json.load(f)

    return {
        k: Job(
            id=v["id"],
            text=v["text"],
            status=JobStatus(v["status"]),
            audio_path=v.get("audio_path"),
        )
        for k, v in raw.items()
    }


def save_jobs(jobs: dict):
    serializable = {
        k: {
            "id": v.id,
            "text": v.text,
            "status": v.status.value,
            "audio_path": v.audio_path,
        }
        for k, v in jobs.items()
    }

    with open(DB_PATH, "w") as f:
        json.dump(serializable, f, indent=2)