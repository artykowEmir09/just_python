from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Tag, Task
from app.models.base import utcnow
from app.schemas.task import TaskCreate, TaskUpdate

# These fields can't be set to null.
REQUIRED_FIELDS = {"title", "status", "priority"}


def _sync_completed_at(task: Task) -> None:
    """Keep completed_at consistent with status."""
    if task.status == "done":
        if task.completed_at is None:
            task.completed_at = utcnow()
    else:
        task.completed_at = None


def create_task(db: Session, data: TaskCreate) -> Task:
    task = Task(**data.model_dump())
    _sync_completed_at(task)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def list_tasks(db: Session) -> list[Task]:
    return list(db.scalars(select(Task).order_by(Task.id.desc())))


def get_task(db: Session, task_id: int) -> Task | None:
    return db.get(Task, task_id)


def update_task(db: Session, task: Task, data: TaskUpdate) -> Task:
    changes = data.model_dump(exclude_unset=True)
    for field, value in changes.items():
        if value is None and field in REQUIRED_FIELDS:
            continue
        setattr(task, field, value)
    if "status" in changes:
        _sync_completed_at(task)
    db.commit()
    db.refresh(task)
    return task


def complete_task(db: Session, task: Task) -> Task:
    task.status = "done"
    _sync_completed_at(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task: Task) -> None:
    db.delete(task)
    db.commit()


def attach_tag(db: Session, task: Task, tag: Tag) -> Task:
    if tag not in task.tags:
        task.tags.append(tag)
        db.commit()
        db.refresh(task)
    return task


def detach_tag(db: Session, task: Task, tag: Tag) -> Task:
    if tag in task.tags:
        task.tags.remove(tag)
        db.commit()
        db.refresh(task)
    return task
