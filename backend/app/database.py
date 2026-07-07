from pymongo import AsyncMongoClient
from backend.app.config import settings


_client: AsyncMongoClient | None = None

def init_database():
    global _client
    _client = AsyncMongoClient(settings.MONGODB_URI)
    return _client

def get_db():
    if _client is None:
        raise RuntimeError("Database not initialized")
    return _client[settings.MONGODB_NAME]

def close_database():
    global _client
    if _client:
        _client.close()