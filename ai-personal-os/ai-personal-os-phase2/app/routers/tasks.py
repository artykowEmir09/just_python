from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.task import TaskCreate, TaskRead, TaskUpdate
from app.services import tag_service, task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def _get_task_or_404(db: Session, task_id: int):
    task = task_service.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


def _get_tag_or_404(db: Session, tag_id: int):
    tag = tag_service.get_tag(db, tag_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(data: TaskCreate, db: Session = Depends(get_db)):
    return task_service.create_task(db, data)


@router.get("", response_model=list[TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    return task_service.list_tasks(db)


@router.get("/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return _get_task_or_404(db, task_id)


@router.put("/{task_id}", response_model=TaskRead)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db)):
    task = _get_task_or_404(db, task_id)
    return task_service.update_task(db, task, data)


@router.patch("/{task_id}/complete", response_model=TaskRead)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    task = _get_task_or_404(db, task_id)
    return task_service.complete_task(db, task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = _get_task_or_404(db, task_id)
    task_service.delete_task(db, task)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/{task_id}/tags/{tag_id}", response_model=TaskRead)
def attach_tag(task_id: int, tag_id: int, db: Session = Depends(get_db)):
    task = _get_task_or_404(db, task_id)
    tag = _get_tag_or_404(db, tag_id)
    return task_service.attach_tag(db, task, tag)


@router.delete("/{task_id}/tags/{tag_id}", response_model=TaskRead)
def detach_tag(task_id: int, tag_id: int, db: Session = Depends(get_db)):
    task = _get_task_or_404(db, task_id)
    tag = _get_tag_or_404(db, tag_id)
    return task_service.detach_tag(db, task, tag)
