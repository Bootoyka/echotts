from datetime import datetime, timezone
from backend.app import worker_crud
from backend.app.jobs import JobStatus
from backend.app.logger import logger
from backend.app.queue import dequeue
from backend.app.tts import generate_audio


def worker():
    logger.info("Worker started")

    while True:
        job_id = dequeue()

        logger.info("Received job %s", job_id)

        job = worker_crud.get_job(job_id)

        if not job:
            logger.error("Job not found: %s", job_id)
            continue

        try:
            job.status = JobStatus.PROCESSING
            job.started_at = datetime.now(timezone.utc)
            worker_crud.save_job(job)

            path = generate_audio(job.text, job.id)

            job.status = JobStatus.DONE
            job.audio_path = path
            job.completed_at = datetime.now(timezone.utc)

            worker_crud.save_job(job)

        except Exception:
            job.status = JobStatus.FAILED
            worker_crud.save_job(job)

            logger.exception("Job failed: %s", job.id)
