from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import verify_token
from app.database import get_db
from app.models import Label
from app.schemas import LabelCreate, LabelResponse, LabelUpdate

router = APIRouter()


@router.get("/labels", response_model=List[LabelResponse])
def list_labels(
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    return db.query(Label).all()


@router.post("/labels", response_model=LabelResponse, status_code=status.HTTP_201_CREATED)
def create_label(
    payload: LabelCreate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    label = Label(**payload.model_dump())
    db.add(label)
    db.commit()
    db.refresh(label)
    return label


@router.get("/labels/{label_id}", response_model=LabelResponse)
def get_label(
    label_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    label = db.query(Label).filter(Label.id == label_id).first()
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    return label


@router.put("/labels/{label_id}", response_model=LabelResponse)
def update_label(
    label_id: int,
    payload: LabelUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    label = db.query(Label).filter(Label.id == label_id).first()
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(label, field, value)
    db.commit()
    db.refresh(label)
    return label


@router.delete("/labels/{label_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_label(
    label_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(verify_token),
):
    label = db.query(Label).filter(Label.id == label_id).first()
    if not label:
        raise HTTPException(status_code=404, detail="Label not found")
    db.delete(label)
    db.commit()
