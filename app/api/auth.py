from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app import schemas, models
from app.core.security import get_password_hash, verify_password, create_access_token, get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])

# Регистрация пользователей (с хешированием пароля)
@router.post("/register", response_model=schemas.UserRead)
def register(user_create: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(user_create.email == models.User.email).first()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user_create.password)
    new_user = models.User(email=user_create.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Аутентификация пользователей (выдача JWT-токена при входе)
@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(form_data.username == models.User.email).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect email or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
