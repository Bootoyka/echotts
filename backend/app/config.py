from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGODB_URI: str
    MONGODB_NAME: str = "echotts_db"
    MODEL_PATH: str
    CONFIG_PATH: str
    AUDIO_DIR: Path=Path(__file__).resolve().parent.parent.parent / "data"/ "audio"
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    QUEUE_NAME: str = "tts_jobs"

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parent.parent / ".env",
        env_file_encoding="utf-8",
    )

settings = Settings()