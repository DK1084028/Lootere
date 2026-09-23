import urllib.parse
from typing import Optional
from fastapi import APIRouter, Depends, Header, HTTPException, status
from fastapi.responses import StreamingResponse
from motor.motor_asyncio import AsyncIOMotorDatabase
from backend.database.connection import get_db
from backend.services.stream_service import generate_media_stream

router = APIRouter(prefix="/api/v1/stream", tags=["Media Streaming"])

@router.get("/{file_id}")
async def stream_video(file_id: str, range: Optional[str] = Header(None), db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        stream_gen, start, end, file_size, mime_type, file_name = await generate_media_stream(db, file_id, range)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    content_length = (end - start) + 1
    headers = {
        "Content-Range": f"bytes {start}-{end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": str(content_length),
        "Content-Type": mime_type,
        "Access-Control-Allow-Origin": "*",
    }
    status_code = status.HTTP_206_PARTIAL_CONTENT if range else status.HTTP_200_OK
    return StreamingResponse(stream_gen, status_code=status_code, headers=headers, media_type=mime_type)
