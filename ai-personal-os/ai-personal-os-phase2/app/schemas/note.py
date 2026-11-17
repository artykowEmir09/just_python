from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.tag import TagRead


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = ""


class NoteUpdate(BaseModel):
    """All fields optional: send only what you want to change."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    content: Optional[str] = None
    is_archived: Optional[bool] = None


class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    is_archived: bool
    ai_summary: Optional[str] = None
    tags: list[TagRead] = []
    created_at: datetime
    updated_at: datetime
