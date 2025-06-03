from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# User schemas

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


# Book schemas

class BookBase(BaseModel):
    title: str
    author: str
    year: Optional[int] = None
    isbn: Optional[str] = None
    copies: int = Field(default=1, ge=0)
    description: Optional[str] = None


class BookCreate(BookBase):
    pass


class BookRead(BookBase):
    id: int

    class Config:
        orm_mode = True


# Reader schemas

class ReaderBase(BaseModel):
    name: str
    email: EmailStr


class ReaderCreate(ReaderBase):
    pass


class ReaderRead(ReaderBase):
    id: int

    class Config:
        orm_mode = True

class BookUpdate(BookBase):
    pass

# BorrowedBook schemas

class BorrowedBookRead(BaseModel):
    id: int
    book_id: int
    reader_id: int
    borrow_date: datetime
    return_date: Optional[datetime]

    class Config:
        orm_mode = True
