from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..deps import get_current_active_user
from ..models import Answer, ExpertProfile, Question, User
from ..schemas.answer import AnswerOut
from ..schemas.question import QuestionOut
from ..schemas.user import (
    ExpertProfilePublic,
    ExpertProfileUpdate,
    UserDirectoryProfile,
    UserProfileResponse,
)
from .questions import answer_to_schema, question_to_schema

router = APIRouter(prefix="/users", tags=["users"])


def _get_user_or_404(db: Session, user_id: str) -> User:
    user = (
        db.query(User)
        .options(joinedload(User.expert_profile))
        .filter(User.id == user_id)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get("/me", response_model=UserProfileResponse)
def get_current_user_profile(
    current_user: User = Depends(get_current_active_user),
) -> UserProfileResponse:
    return UserProfileResponse.model_validate(current_user, from_attributes=True)


@router.put("/me/profile", response_model=ExpertProfilePublic)
def update_expert_profile(
    payload: ExpertProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ExpertProfilePublic:
    profile = current_user.expert_profile

    if not profile:
        profile = ExpertProfile(user_id=current_user.id)
        db.add(profile)

    if payload.full_name is not None:
        profile.full_name = payload.full_name
    if payload.bio is not None:
        profile.bio = payload.bio
    if payload.primary_role is not None:
        profile.primary_role = payload.primary_role
    if payload.skills is not None:
        profile.skills = payload.skills
    if payload.github_url is not None:
        profile.github_url = payload.github_url
    if payload.linkedin_url is not None:
        profile.linkedin_url = payload.linkedin_url
    if payload.portfolio_url is not None:
        profile.portfolio_url = payload.portfolio_url
    if payload.experience_years is not None:
        profile.experience_years = payload.experience_years

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return ExpertProfilePublic.model_validate(profile, from_attributes=True)


@router.get("/experts", response_model=List[UserDirectoryProfile])
def list_experts(db: Session = Depends(get_db)) -> List[UserDirectoryProfile]:
    experts = (
        db.query(User)
        .outerjoin(ExpertProfile)
        .filter(
            (User.role == "expert") | (ExpertProfile.id.isnot(None)),
            User.is_active.is_(True),
        )
        .all()
    )
    return [
        UserDirectoryProfile.model_validate(expert, from_attributes=True)
        for expert in experts
    ]


@router.get("/profile/{user_id}", response_model=UserDirectoryProfile)
def get_user_public_profile(
    user_id: str, db: Session = Depends(get_db)
) -> UserDirectoryProfile:
    user = _get_user_or_404(db, user_id)
    return UserDirectoryProfile.model_validate(user, from_attributes=True)


@router.get("/{user_id}", response_model=UserDirectoryProfile)
def get_user_public_profile_alias(
    user_id: str, db: Session = Depends(get_db)
) -> UserDirectoryProfile:
    reserved_prefixes = {"me", "experts", "profile"}
    if user_id in reserved_prefixes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")
    user = _get_user_or_404(db, user_id)
    return UserDirectoryProfile.model_validate(user, from_attributes=True)


@router.get("/me/questions", response_model=List[QuestionOut])
def list_my_questions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[QuestionOut]:
    questions = (
        db.query(Question)
        .options(
            joinedload(Question.client).joinedload(User.expert_profile),
            joinedload(Question.answers),
        )
        .filter(Question.client_id == current_user.id)
        .order_by(Question.created_at.desc())
        .all()
    )
    return [question_to_schema(question) for question in questions]


@router.get("/me/answers", response_model=List[AnswerOut])
def list_my_answers(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[AnswerOut]:
    answers = (
        db.query(Answer)
        .options(
            joinedload(Answer.author),
            joinedload(Answer.question)
            .joinedload(Question.client)
            .joinedload(User.expert_profile),
            joinedload(Answer.author).joinedload(User.answers),
        )
        .filter(Answer.author_id == current_user.id)
        .order_by(Answer.created_at.desc())
        .all()
    )
    return [answer_to_schema(answer) for answer in answers]

