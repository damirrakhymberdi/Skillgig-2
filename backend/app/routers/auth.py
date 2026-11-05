from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy import or_
from sqlalchemy.orm import Session

from ..core.config import get_settings
from ..database import get_db
from ..models import ExpertProfile, User
from ..schemas.auth import RegisterResponse, RefreshRequest, TokenResponse
from ..schemas.user import UserCreate, UserPublic
from ..utils.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_password_hash,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()


def _get_user_by_identifier(db: Session, identifier: str) -> User | None:
    return (
        db.query(User)
        .filter(
            or_(
                User.email == identifier.lower(),
                User.username == identifier,
            )
        )
        .first()
    )


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(payload: UserCreate, db: Session = Depends(get_db)) -> RegisterResponse:
    duplicate_conditions = [User.email == payload.email.lower()]
    if payload.username is not None:
        duplicate_conditions.append(User.username == payload.username)
    existing_user = (
        db.query(User)
        .filter(or_(*duplicate_conditions))
        .first()
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists",
        )

    user = User(
        email=payload.email.lower(),
        username=payload.username,
        first_name=payload.first_name,
        last_name=payload.last_name,
        role=payload.role or "client",
        hashed_password=get_password_hash(payload.password),
    )

    full_name_parts = [payload.first_name or "", payload.last_name or ""]
    full_name = " ".join(part for part in full_name_parts if part).strip() or None

    if user.role == "expert" and full_name:
        profile = ExpertProfile(
            user=user,
            full_name=full_name,
            primary_role="expert",
            skills=[],
        )
        db.add(profile)

    db.add(user)
    db.commit()
    db.refresh(user)
    return RegisterResponse(user=UserPublic.model_validate(user, from_attributes=True))


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:
    identifier = form_data.username
    user = _get_user_by_identifier(db, identifier)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return TokenResponse(
        access_token=access_token["token"],
        refresh_token=refresh_token["token"],
        token_type="Bearer",
        expires_in=settings.access_token_expire_minutes * 60,
        user=UserPublic.model_validate(user, from_attributes=True),
    )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    payload: RefreshRequest, db: Session = Depends(get_db)
) -> TokenResponse:
    try:
        token_payload = decode_token(payload.refresh_token, expected_type="refresh")
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        ) from exc

    user_id = token_payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    return TokenResponse(
        access_token=access_token["token"],
        refresh_token=refresh_token["token"],
        token_type="Bearer",
        expires_in=settings.access_token_expire_minutes * 60,
        user=UserPublic.model_validate(user, from_attributes=True),
    )

