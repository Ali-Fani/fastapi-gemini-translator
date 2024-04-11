from functools import lru_cache
import os

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlmodel import SQLModel, create_engine
# from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator

from sqlalchemy.orm import sessionmaker

from config.config import Settings

@lru_cache
def get_settings():
    return Settings()

# DATABASE_URL = os.environ.get("DATABASE_URL_2")

engine = AsyncEngine(create_engine(get_settings().database_url, echo=True, future=True))


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session