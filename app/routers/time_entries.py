from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import verify_token
from app.database import get_db
from app.models import Task, TimeEntry
from app.schemas import TimeEntryCreate, TimeEntryResponse, TimeEntryUpdate

router = APIRouter()


@router.get("/time-entries", response_model=List[TimeEntryResponse])
def list_time_entries(
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    return db.query(TimeEntry).all()


@router.post("/time-entries", response_model=TimeEntryResponse, status_code=status.HTTP_201_CREATED)
def create_time_entry(
    payload: TimeEntryCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    if not db.query(Task).filter(Task.id == payload.task_id).first():
        raise HTTPException(status_code=404, detail="Task not found")
    entry = TimeEntry(**payload.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.get("/time-entries/{entry_id}", response_model=TimeEntryResponse)
def get_time_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    entry = db.query(TimeEntry).filter(TimeEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Time entry not found")
    return entry


@router.put("/time-entries/{entry_id}", response_model=TimeEntryResponse)
def update_time_entry(
    entry_id: int,
    payload: TimeEntryUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    entry = db.query(TimeEntry).filter(TimeEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Time entry not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(entry, field, value)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/time-entries/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_time_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    entry = db.query(TimeEntry).filter(TimeEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Time entry not found")
    db.delete(entry)
    db.commit()
