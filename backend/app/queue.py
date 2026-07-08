from redis import Redis
from backend.app.config import settings

redis = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
    socket_timeout=None,
)

QUEUE_NAME = settings.QUEUE_NAME

def enqueue(job_id: str):
    redis.lpush(QUEUE_NAME, job_id)

def dequeue() -> str:
    result = redis.brpop(QUEUE_NAME)

    if result is None:
        raise RuntimeError("Redis queue returned no job")

    _, job_id = result

    return job_id
