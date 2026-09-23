import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENV: str = os.getenv("ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    PROJECT_NAME: str = "LOOTERE"
    PORT: int = int(os.getenv("PORT", 8000))

    TELEGRAM_API_ID: int = int(os.getenv("TELEGRAM_API_ID", "0"))
    TELEGRAM_API_HASH: str = os.getenv("TELEGRAM_API_HASH", "")
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")

    MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "lootere_db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    TMDB_API_KEY: str = os.getenv("TMDB_API_KEY", "")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-key")

settings = Settings()
