from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.note import NoteCreate, NoteRead, NoteUpdate
from app.services import note_service, tag_service

router = APIRouter(prefix="/notes", tags=["Notes"])


def _get_note_or_404(db: Session, note_id: int):
    note = note_service.get_note(db, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


def _get_tag_or_404(db: Session, tag_id: int):
    tag = tag_service.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.post("", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
def create_note(data: NoteCreate, db: Session = Depends(get_db)):
    return note_service.create_note(db, data)


@router.get("", response_model=list[NoteRead])
def list_notes(db: Session = Depends(get_db)):
    return note_service.list_notes(db)


@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, db: Session = Depends(get_db)):
    return _get_note_or_404(db, note_id)


@router.put("/{note_id}", response_model=NoteRead)
def update_note(note_id: int, data: NoteUpdate, db: Session = Depends(get_db)):
    note = _get_note_or_404(db, note_id)
    return note_service.update_note(db, note, data)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = _get_note_or_404(db, note_id)
    note_service.delete_note(db, note)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{note_id}/tags/{tag_id}", response_model=NoteRead)
def attach_tag(note_id: int, tag_id: int, db: Session = Depends(get_db)):
    note = _get_note_or_404(db, note_id)
    tag = _get_tag_or_404(db, tag_id)
    return note_service.attach_tag(db, note, tag)


@router.delete("/{note_id}/tags/{tag_id}", response_model=NoteRead)
def detach_tag(note_id: int, tag_id: int, db: Session = Depends(get_db)):
    note = _get_note_or_404(db, note_id)
    tag = _get_tag_or_404(db, tag_id)
    return note_service.detach_tag(db, note, tag)
