import asyncio
import logging
from pyrogram import Client
from backend.config import settings
from backend.database.connection import connect_to_databases, close_database_connections

app = Client("lootere_bot", api_id=settings.TELEGRAM_API_ID, api_hash=settings.TELEGRAM_API_HASH, bot_token=settings.BOT_TOKEN)

async def main():
    await connect_to_databases()
    await app.start()
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
