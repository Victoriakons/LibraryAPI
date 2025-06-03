from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas, models
from app.core.security import get_db, get_current_user

router = APIRouter(prefix="/api/readers", tags=["readers"])

@router.post("/", response_model=schemas.ReaderRead, status_code=status.HTTP_201_CREATED)
def create_reader(reader: schemas.ReaderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    db_reader = db.query(models.Reader).filter(models.Reader.email == reader.email).first()
    if db_reader:
        raise HTTPException(status_code=400, detail="Reader with this email already exists")
    new_reader = models.Reader(**reader.dict())
    db.add(new_reader)
    db.commit()
    db.refresh(new_reader)
    return new_reader

@router.get("/", response_model=List[schemas.ReaderRead])
def list_readers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user=Depends(get_current_user)):
    readers = db.query(models.Reader).offset(skip).limit(limit).all()
    return readers

@router.get("/{reader_id}", response_model=schemas.ReaderRead)
def get_reader(reader_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader

@router.put("/{reader_id}", response_model=schemas.ReaderRead)
def update_reader(reader_id: int, reader_update: schemas.ReaderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    for field, value in reader_update.dict().items():
        setattr(reader, field, value)
    db.commit()
    db.refresh(reader)
    return reader

@router.delete("/{reader_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reader(reader_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    db.delete(reader)
    db.commit()
    return
