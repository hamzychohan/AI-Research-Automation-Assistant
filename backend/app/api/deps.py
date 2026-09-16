import uuid
from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
import redis

from app.core.config import settings
from app.core.database import get_db
from app.core.redis import get_redis_client
from app.models.user import User
from app.schemas.auth import TokenData

# OAuth2 scheme config specifying the token route
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

def get_redis() -> Generator[redis.Redis, None, None]:
    """FastAPI Dependency yielding an active Redis client connection."""
    client = get_redis_client()
    try:
        yield client
    finally:
        client.close()

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """FastAPI Dependency for authenticating HTTP request tokens."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
        
    user = db.query(User).filter(User.id == uuid.UUID(token_data.user_id)).first()
    if user is None:
        raise credentials_exception
    return user

def get_user_from_token(token: str, db: Session) -> User or None:
    """Helper method to authenticate tokens manually, useful for WebSockets query checking."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return db.query(User).filter(User.id == uuid.UUID(user_id)).first()
    except Exception:
        return None
