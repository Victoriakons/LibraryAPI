from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas
from app.core.security import get_db, get_current_user
from app.crud import crud_books  # Импортируем наш CRUD

router = APIRouter(prefix="/api/books", tags=["books"])

@router.post("/", response_model=schemas.BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    try:
        return crud_books.create_book(db, book)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[schemas.BookRead])
def list_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user=Depends(get_current_user)):
    books = crud_books.get_books(db)
    return books[skip:skip + limit]  # Обработка skip и limit здесь

@router.get("/{book_id}", response_model=schemas.BookRead)
def get_book(book_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    book = crud_books.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=schemas.BookRead)
def update_book(book_id: int, book_update: schemas.BookCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    updated_book = crud_books.update_book(db, book_id, book_update)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    success = crud_books.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return
