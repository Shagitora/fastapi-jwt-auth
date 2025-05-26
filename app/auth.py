from datetime import datetime, timedelta
from jose import JWTError, jwt # для создания и валидации JWT-токенов
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import models
from app.database import SessionLocal
from app.config import settings # Конфигурация из .env
from app.utils import verify_password

# OAuth2 схема, где токен ожидается в заголовке Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Подключение к БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta # Задаем срок жизни токена
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")

def create_tokens(username: str):  # "sub": username - стандартное поле в JWT, обозначающее "subject" токена - т.е. владельца
    access_token = create_token({"sub": username}, timedelta(minutes=settings.access_token_expire_minutes))
    refresh_token = create_token({"sub": username}, timedelta(minutes=settings.refresh_token_expire_minutes))
    return access_token, refresh_token
    
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    try: # Декодируем JWT
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user