from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.core.security import get_db, get_current_user
from app.crud import crud_borrow  # 💡 добавим импорт
from app import models


router = APIRouter(prefix="/api/borrow", tags=["borrow"])


@router.post("/", response_model=schemas.BorrowedBookRead, status_code=status.HTTP_201_CREATED)
def borrow_book(
    book_id: int = Query(...),
    reader_id: int = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    borrow = crud_borrow.issue_book(db, book_id, reader_id)
    if borrow is None:
        raise HTTPException(status_code=400, detail="Cannot borrow book (limit or availability)")
    return borrow


@router.post("/{borrow_id}/return", response_model=schemas.BorrowedBookRead)
def return_book(
    borrow_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # Получим саму запись
    borrow = db.query(models.BorrowedBook).filter(models.BorrowedBook.id == borrow_id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    if borrow.return_date is not None:
        raise HTTPException(status_code=400, detail="Book already returned")

    returned = crud_borrow.return_book(db, book_id=borrow.book_id, reader_id=borrow.reader_id)
    if not returned:
        raise HTTPException(status_code=400, detail="Could not return book")
    return returned


@router.get("/", response_model=List[schemas.BorrowedBookRead])
def list_borrows(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return db.query(models.BorrowedBook).offset(skip).limit(limit).all()

