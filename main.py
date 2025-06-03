from fastapi import FastAPI

from app.api import auth, books, borrow, readers
from app.db.base import Base
from app.db.session import engine


Base.metadata.create_all(bind=engine)

app = FastAPI(title="LibraryAPI")

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(readers.router)
app.include_router(borrow.router)
