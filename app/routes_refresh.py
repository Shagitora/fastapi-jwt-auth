from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from app.auth import get_user_by_username, create_tokens, get_db
from app.config import settings
from app import schemas


router = APIRouter()

@router.post("/refresh", response_model=schemas.Token)
def refresh_token(refresh_token: str = Body(..., embed=True), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(refresh_token, settings.secret_key, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception

    new_access_token, new_refresh_token = create_tokens(username)
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }

