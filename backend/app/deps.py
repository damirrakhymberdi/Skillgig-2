from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from .core.config import get_settings
from .database import get_db
from .models.user import User
from .utils.security import decode_token

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.api_prefix}/auth/login")
optional_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.api_prefix}/auth/login", auto_error=False
)


def _user_from_token(db: Session, token: str) -> User:
    try:
        payload = decode_token(token, expected_type="access")
        user_id = payload.get("sub")
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        ) from exc

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    return _user_from_token(db, token)


def get_optional_current_user(
    db: Session = Depends(get_db),
    token: Optional[str] = Depends(optional_oauth2_scheme),
) -> Optional[User]:
    return _user_from_token(db, token) if token else None


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )
    return current_user

