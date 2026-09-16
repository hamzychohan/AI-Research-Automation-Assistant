from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import get_password_hash, verify_password

def get_user_by_email(db: Session, email: str) -> User or None:
    """Retrieves a user object from the database using their email."""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, email: str, password: str) -> User:
    """Creates a new user record with hashed password security."""
    hashed_password = get_password_hash(password)
    db_user = User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> User or None:
    """Verifies user credentials against stored credentials."""
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
