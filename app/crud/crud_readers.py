from sqlalchemy.orm import Session
from app.models import Reader
from app.schemas import ReaderCreate, ReaderUpdate

def get_readers(db: Session):
    return db.query(Reader).all()

def get_reader(db: Session, reader_id: int):
    return db.query(Reader).filter(Reader.id == reader_id).first()

def create_reader(db: Session, reader_in: ReaderCreate):
    db_reader = Reader(**reader_in.dict())
    db.add(db_reader)
    db.commit()
    db.refresh(db_reader)
    return db_reader

def update_reader(db: Session, reader_id: int, reader_in: ReaderUpdate):
    reader = get_reader(db, reader_id)
    if not reader:
        return None
    for field, value in reader_in.dict(exclude_unset=True).items():
        setattr(reader, field, value)
    db.commit()
    db.refresh(reader)
    return reader

def delete_reader(db: Session, reader_id: int):
    reader = get_reader(db, reader_id)
    if not reader:
        return False
    db.delete(reader)
    db.commit()
    return True