from sqlalchemy.orm import Session
from app.models import Book
from app.schemas import BookCreate, BookUpdate

def get_books(db: Session):
    return db.query(Book).all()

def get_book(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def create_book(db: Session, book_in: BookCreate):
    db_book = Book(**book_in.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book_in: BookUpdate):
    book = get_book(db, book_id)
    if not book:
        return None
    for field, value in book_in.dict(exclude_unset=True).items():
        setattr(book, field, value)
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, book_id: int):
    book = get_book(db, book_id)
    if not book:
        return False
    db.delete(book)
    db.commit()
    return True