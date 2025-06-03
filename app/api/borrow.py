from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app import schemas, models
from app.core.security import get_db, get_current_user

router = APIRouter(prefix="/api/borrow", tags=["borrow"])


@router.post("/", response_model=schemas.BorrowedBookRead, status_code=status.HTTP_201_CREATED)
def borrow_book(
    book_id: int = Query(...),
    reader_id: int = Query(...),
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    reader = db.query(models.Reader).filter(models.Reader.id == reader_id).first()
    if not reader:
        raise HTTPException(status_code=404, detail="Reader not found")

    active_borrows_count = db.query(models.BorrowedBook).filter(
        models.BorrowedBook.book_id == book_id,
        models.BorrowedBook.return_date == None
    ).count()
    if active_borrows_count >= book.copies:
        raise HTTPException(status_code=400, detail="No available copies to borrow")

    # ✅ Добавляем явное указание времени, чтобы избежать конфликта unique-constraint
    borrow = models.BorrowedBook(
        book_id=book_id,
        reader_id=reader_id,
        borrow_date=datetime.utcnow()
    )
    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return borrow


@router.post("/{borrow_id}/return", response_model=schemas.BorrowedBookRead)
def return_book(borrow_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    borrow = db.query(models.BorrowedBook).filter(models.BorrowedBook.id == borrow_id).first()
    if not borrow:
        raise HTTPException(status_code=404, detail="Borrow record not found")
    if borrow.return_date is not None:
        raise HTTPException(status_code=400, detail="Book already returned")
    borrow.return_date = datetime.utcnow()
    db.commit()
    db.refresh(borrow)
    return borrow


@router.get("/", response_model=List[schemas.BorrowedBookRead])
def list_borrows(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user=Depends(get_current_user)):
    borrows = db.query(models.BorrowedBook).offset(skip).limit(limit).all()
    return borrows
