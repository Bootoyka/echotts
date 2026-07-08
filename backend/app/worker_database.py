from pymongo import MongoClient
from backend.app.config import settings


client = MongoClient(settings.MONGODB_URI)

db = client[settings.MONGODB_NAME]


def get_worker_db():
    return db


def close_worker_database():
    client.close()

def check_worker_database():
    client.admin.command("ping")