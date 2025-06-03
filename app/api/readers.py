from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas
from app.core.security import get_db, get_current_user
from app.crud import crud_readers

router = APIRouter(prefix="/api/readers", tags=["readers"])

@router.post("/", response_model=schemas.ReaderRead, status_code=status.HTTP_201_CREATED)
def create_reader(reader: schemas.ReaderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    existing = db.query(crud_readers.Reader).filter(crud_readers.Reader.email == reader.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Reader with this email already exists")
    return crud_readers.create_reader(db, reader)

@router.get("/", response_model=List[schemas.ReaderRead])
def list_readers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return crud_readers.get_readers(db)

@router.get("/{reader_id}", response_model=schemas.ReaderRead)
def get_reader(reader_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    reader = crud_readers.get_reader(db, reader_id)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader

@router.put("/{reader_id}", response_model=schemas.ReaderRead)
def update_reader(reader_id: int, reader_update: schemas.ReaderCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    reader = crud_readers.update_reader(db, reader_id, reader_update)
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")
    return reader

@router.delete("/{reader_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reader(reader_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    success = crud_readers.delete_reader(db, reader_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reader not found")
    return

