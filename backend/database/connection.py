import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from backend.config import settings

logger = logging.getLogger("lootere-db")

class DatabaseManager:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

db_manager = DatabaseManager()

async def connect_to_databases():
    db_manager.client = AsyncIOMotorClient(settings.MONGO_URI)
    db_manager.db = db_manager.client[settings.MONGO_DB_NAME]
    logger.info("MongoDB connection established.")

async def close_database_connections():
    if db_manager.client:
        db_manager.client.close()

async def get_db() -> AsyncIOMotorDatabase:
    return db_manager.db
