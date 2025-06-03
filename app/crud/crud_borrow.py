from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from typing import List
from app.models import BorrowedBook, Book
from app.schemas import BorrowOut

MAX_BORROWED_BOOKS = 3

def issue_book(db: Session, book_id: int, reader_id: int):
    # Проверяем доступность книги
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book or book.copies < 1:
        return None  # Нет доступных экземпляров

    # Проверяем сколько книг уже взял читатель
    active_borrows = db.query(BorrowedBook).filter(
        BorrowedBook.reader_id == reader_id,
        BorrowedBook.return_date.is_(None)
    ).count()

    if active_borrows >= MAX_BORROWED_BOOKS:
        return None  # Превышен лимит

    # Создаем запись выдачи
    borrow = BorrowedBook(
        book_id=book_id,
        reader_id=reader_id,
        borrow_date=datetime.utcnow(),
        return_date=None
    )

    book.copies -= 1  # уменьшаем количество доступных экземпляров
    db.add(borrow)
    db.commit()
    db.refresh(borrow)
    return borrow

def return_book(db: Session, book_id: int, reader_id: int):
    # Ищем активную выдачу книги читателю
    borrow = db.query(BorrowedBook).filter(
        BorrowedBook.book_id == book_id,
        BorrowedBook.reader_id == reader_id,
        BorrowedBook.return_date.is_(None)
    ).first()

    if not borrow:
        return None  # Книга не выдана или уже возвращена

    borrow.return_date = datetime.utcnow()

    # Увеличиваем количество доступных экземпляров
    book = db.query(Book).filter(Book.id == book_id).first()
    if book:
        book.copies += 1

    db.commit()
    db.refresh(borrow)
    return borrow

def get_borrowed_books_by_reader(db: Session, reader_id: int) -> List[BorrowOut]:
    borrows = db.query(BorrowedBook).filter(
        BorrowedBook.reader_id == reader_id,
        BorrowedBook.return_date.is_(None)
    ).all()
    return borrows