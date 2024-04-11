import uuid

from sqlalchemy import Column, DateTime, func
# from sqlalchemy import Column
from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime, timezone
import sqlalchemy as sa


class TranslationRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    rich_text: str
    source_language: str
    target_language: str
    translated_text: Optional[str] = None
    status: str = "PENDING"
    callback_url: str
    request_id: str = Field(default_factory=lambda: str(uuid.uuid4()), nullable=False, unique=True)
    created_at: Optional[datetime] 
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime] = None
    retries: int = 0
    token_count: Optional[int]
    # api_key_id: int = Field(foreign_key="apikey.id", nullable=False)  # New field added here


# class APIKey(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     key: str = Field(index=True, nullable=False)
#     created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
#     is_active: bool = Field(default=True)

# class RateLimit(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     api_key_id: int = Field(foreign_key="apikey.id", nullable=False)
#     endpoint: str = Field(nullable=False)
#     count: int = Field(default=0)
#     period_start: datetime = Field(default_factory=datetime.now(timezone.utc))

