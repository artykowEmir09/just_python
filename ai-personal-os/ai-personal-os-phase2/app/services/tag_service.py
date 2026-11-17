from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Tag


def create_tag(db: Session, name: str) -> Tag:
    tag = Tag(name=name)
    db.add(tag)
    db.commit()
    db.refresh(tag)
    return tag


def get_tag_by_name(db: Session, name: str) -> Tag | None:
    return db.scalar(select(Tag).where(Tag.name == name))


def list_tags(db: Session) -> list[Tag]:
    return list(db.scalars(select(Tag).order_by(Tag.name)))


def get_tag(db: Session, tag_id: int) -> Tag | None:
    return db.get(Tag, tag_id)


def delete_tag(db: Session, tag: Tag) -> None:
    db.delete(tag)
    db.commit()
