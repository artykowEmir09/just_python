from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Note, Tag
from app.schemas.note import NoteCreate, NoteUpdate


def create_note(db: Session, data: NoteCreate) -> Note:
    note = Note(**data.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def list_notes(db: Session) -> list[Note]:
    return list(db.scalars(select(Note).order_by(Note.id.desc())))


def get_note(db: Session, note_id: int) -> Note | None:
    return db.get(Note, note_id)


def update_note(db: Session, note: Note, data: NoteUpdate) -> Note:
    for field, value in data.model_dump(exclude_unset=True).items():
        if value is not None:  # none of the note fields can be set to null
            setattr(note, field, value)
    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, note: Note) -> None:
    db.delete(note)
    db.commit()


def attach_tag(db: Session, note: Note, tag: Tag) -> Note:
    if tag not in note.tags:
        note.tags.append(tag)
        db.commit()
        db.refresh(note)
    return note


def detach_tag(db: Session, note: Note, tag: Tag) -> Note:
    if tag in note.tags:
        note.tags.remove(tag)
        db.commit()
        db.refresh(note)
    return note
