import asyncio
from datetime import datetime
from functools import lru_cache
from typing import Annotated, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import func
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session, init_db
from config.config import Settings

from app.models import TranslationRequest

from app.tasks import translate_in_background
import sentry_sdk


@lru_cache
def get_settings():
    return Settings()


# from app.models import Song, SongCreate
sentry_sdk.init(
    dsn=get_settings().sentry_dsn,
    enable_tracing=True,
    profiles_sample_rate=0.3,

)




app = FastAPI()



@app.get("/ping")
async def pong():
    return {"ping": "pong!"}



@app.post("/translate")
async def translate(rich_text: str,source_language: str,target_language: str,callback_url: str,request_id: Optional[str] = None, db: AsyncSession = Depends(get_session)):
    if request_id is not None:
        existing_request = await db.execute(select(TranslationRequest).where(TranslationRequest.request_id == request_id))
        existing_request = existing_request.scalars().first()
        if existing_request:
            # If a duplicate request_id is found, return an error response
            raise HTTPException(status_code=400, detail="Duplicate request_id. A translation request with this request_id already exists.")
    # Create a new translation request
    new_request = TranslationRequest(rich_text=rich_text,source_language=source_language,target_language=target_language,callback_url=callback_url,request_id=request_id,created_at=datetime.utcnow())
    db.add(new_request)
    await db.commit()

    # Schedule translation in the background
    asyncio.create_task(translate_in_background(new_request.id, rich_text, db))  # No need to copy session

    return {"message": "Translation request submitted. You can check status for completion.", "request_id": new_request.request_id, "status": "submitted"}


@app.get("/translate/{request_id}")
async def get_translation_status(request_id: int, db: AsyncSession = Depends(get_session)):
    request = await db.get(TranslationRequest, request_id)  # Use await for asynchronous query
    if not request:
        raise HTTPException(status_code=404, detail="Translation request not found")

    return {"status": request.status, "translated_text": request.translated_text if request.status == "completed" else None}
# @app.get("/songs", response_model=list[Song])
# async def get_songs(session: AsyncSession = Depends(get_session)):
#     result = await session.execute(select(Song))
#     songs = result.scalars().all()
#     return [Song(name=song.name, artist=song.artist, year=song.year, id=song.id) for song in songs]
#
#
# @app.post("/songs")
# async def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
#     song = Song(name=song.name, artist=song.artist, year=song.year)
#     session.add(song)
#     await session.commit()
#     await session.refresh(song)
#     return song