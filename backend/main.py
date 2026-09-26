import asyncio

# Fix Event Loop for Pyrogram
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pyrogram import Client
from backend.config import settings
from backend.database.connection import connect_to_databases, close_database_connections, db_manager
from backend.services.stream_service import set_pyrogram_client
from backend.api.stream import router as stream_router

stream_pyrogram_client = Client(
    "lootere_streamer",
    api_id=settings.TELEGRAM_API_ID,
    api_hash=settings.TELEGRAM_API_HASH,
    bot_token=settings.BOT_TOKEN
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_databases()
    await stream_pyrogram_client.start()
    set_pyrogram_client(stream_pyrogram_client)
    yield
    await stream_pyrogram_client.stop()
    await close_database_connections()

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(stream_router)

@app.get("/health")
async def health():
    return {"status": "online", "project": settings.PROJECT_NAME}
