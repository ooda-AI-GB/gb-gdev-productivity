from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth import verify_token
from app.database import get_db
from app.models import Comment, Task
from app.schemas import (
    CommentCreate,
    CommentResponse,
    TaskCreate,
    TaskResponse,
    TaskUpdate,
)

router = APIRouter()


@router.get("/tasks", response_model=List[TaskResponse])
def list_tasks(
    assignee: Optional[str] = Query(None, description="Filter by assignee"),
    status: Optional[str] = Query(None, description="Comma-separated statuses, e.g. todo,in_progress"),
    due_before: Optional[date] = Query(None, description="Tasks with due_date < this date"),
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    query = db.query(Task)
    if assignee:
        query = query.filter(Task.assignee == assignee)
    if status:
        statuses = [s.strip() for s in status.split(",") if s.strip()]
        query = query.filter(Task.status.in_(statuses))
    if due_before:
        query = query.filter(Task.due_date < due_before)
    return query.all()


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    task = Task(**payload.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    payload: TaskUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()


# ── Task Comments ─────────────────────────────────────────────────────────────

@router.get("/tasks/{task_id}/comments", response_model=List[CommentResponse])
def list_task_comments(
    task_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    if not db.query(Task).filter(Task.id == task_id).first():
        raise HTTPException(status_code=404, detail="Task not found")
    return db.query(Comment).filter(Comment.task_id == task_id).all()


@router.post(
    "/tasks/{task_id}/comments",
    response_model=CommentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task_comment(
    task_id: int,
    payload: CommentCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    if not db.query(Task).filter(Task.id == task_id).first():
        raise HTTPException(status_code=404, detail="Task not found")
    comment = Comment(task_id=task_id, **payload.model_dump())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment
