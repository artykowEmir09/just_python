from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.tag import TagCreate, TagRead
from app.services import tag_service

router = APIRouter(prefix="/tags", tags=["Tags"])


@router.post("", response_model=TagRead, status_code=status.HTTP_201_CREATED)
def create_tag(data: TagCreate, db: Session = Depends(get_db)):
    if tag_service.get_tag_by_name(db, data.name):
        raise HTTPException(status_code=409, detail="Tag already exists")
    return tag_service.create_tag(db, data.name)


@router.get("", response_model=list[TagRead])
def list_tags(db: Session = Depends(get_db)):
    return tag_service.list_tags(db)


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = tag_service.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    tag_service.delete_tag(db, tag)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
