from typing import Optional

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin
from app.models.tag import note_tags


class Note(TimestampMixin, Base):
    __tablename__ = "notes"

    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text, default="")
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    ai_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    tags = relationship("Tag", secondary=note_tags, back_populates="notes")
