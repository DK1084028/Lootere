import logging
from typing import AsyncGenerator, Optional, Tuple
from pyrogram import Client
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.utils.range_requests import parse_range_header

logger = logging.getLogger("lootere-stream")
pyrogram_client: Optional[Client] = None

def set_pyrogram_client(client: Client):
    global pyrogram_client
    pyrogram_client = client

async def generate_media_stream(
    db: AsyncIOMotorDatabase,
    file_id: str,
    range_header: Optional[str] = None
) -> Tuple[AsyncGenerator[bytes, None], int, int, int, str, str]:
    file_doc = await db.files.find_one({"telegram_file_unique_id": file_id})
    if not file_doc:
        raise ValueError("File not found in index database.")

    file_size = file_doc.get("file_size", 0)
    mime_type = file_doc.get("mime_type", "video/mp4")
    file_name = file_doc.get("file_name", "video.mp4")

    start, end, content_length = parse_range_header(range_header, file_size)

    async def stream_bytes() -> AsyncGenerator[bytes, None]:
        if pyrogram_client is None:
            return
        message = await pyrogram_client.get_messages(
            chat_id=file_doc["source_channel_id"],
            message_ids=file_doc["source_message_id"]
        )
        if not message or not message.media:
            return

        bytes_remaining = content_length
        async for chunk in pyrogram_client.stream_media(message, offset=start, limit=content_length):
            if not chunk:
                break
            yield chunk
            bytes_remaining -= len(chunk)
            if bytes_remaining <= 0:
                break

    return stream_bytes(), start, end, file_size, mime_type, file_name
