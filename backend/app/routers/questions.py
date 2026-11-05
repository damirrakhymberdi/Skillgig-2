from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..deps import get_current_active_user, get_optional_current_user
from ..models import Answer, Question, User, ExpertProfile
from ..schemas.answer import (
    AnswerCreate,
    AnswerModerationRequest,
    AnswerOut,
    AnswerUpdate,
)
from ..schemas.question import (
    QuestionCreate,
    QuestionListResponse,
    QuestionOut,
    QuestionUpdate,
)
from ..schemas.user import ExpertProfilePublic

router = APIRouter(prefix="/questions", tags=["questions"])
PUBLIC_STATUSES = ("published", "resolved")


def _require_visible_question(question: Optional[Question], user: Optional[User]) -> Question:
    if not question or (
        question.status not in PUBLIC_STATUSES
        and (not user or question.client_id != user.id)
    ):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    return question


def _clean_list(values: Optional[List[str]]) -> List[str]:
    if not values:
        return []
    cleaned = []
    for value in values:
        if not value:
            continue
        cleaned.append(value.strip())
    return cleaned


def _client_name(user: Optional[User]) -> str:
    if not user:
        return "Аноним"
    parts = [user.first_name or "", user.last_name or ""]
    full_name = " ".join(part for part in parts if part).strip()
    if full_name:
        return full_name
    return user.username or "Пайдаланушы"


def _profile_to_schema(profile) -> Optional[ExpertProfilePublic]:
    if not profile:
        return None
    return ExpertProfilePublic.model_validate(profile, from_attributes=True)


def _adjust_resolved_questions(user: Optional[User], delta: int) -> None:
    if not user or not user.expert_profile or delta == 0:
        return
    current = user.expert_profile.resolved_questions or 0
    user.expert_profile.resolved_questions = max(0, current + delta)


def _ensure_expert_profile(user: Optional[User], db: Session) -> None:
    if not user:
        return
    if user.expert_profile:
        return
    profile = ExpertProfile(user_id=user.id, resolved_questions=0)
    db.add(profile)
    db.flush()
    user.expert_profile = profile


def question_to_schema(question: Question) -> QuestionOut:
    tags = question.tags or []
    links = question.links or []
    code_link = links[0] if links else None

    is_solved = question.status in {"resolved", "closed"} or bool(
        question.accepted_answer_id
    )

    client = question.client
    client_profile = (
        _profile_to_schema(client.expert_profile) if client else None
    )

    return QuestionOut(
        id=question.id,
        title=question.title,
        description=question.description,
        category=question.category,
        subcategory=question.subcategory,
        difficulty=question.difficulty,
        tags=tags,
        links=links,
        code_link=code_link,
        code_example=question.code_example,
        deadline=question.deadline,
        status=question.status,
        client_id=question.client_id,
        client_name=_client_name(question.client),
        client_role=client.role if client else None,
        client_profile=client_profile,
        answers_count=len(question.answers or []),
        is_solved=is_solved,
        accepted_answer_id=question.accepted_answer_id,
        created_at=question.created_at,
        updated_at=question.updated_at,
    )


def answer_to_schema(answer: Answer) -> AnswerOut:
    author = answer.author
    expert_name = answer.expert_name
    if author and expert_name and expert_name.casefold() == author.email.casefold():
        expert_name = None
    author_profile = (
        _profile_to_schema(author.expert_profile) if author else None
    )
    author_answers_count = len(author.answers or []) if author else 0

    return AnswerOut(
        id=answer.id,
        question_id=answer.question_id,
        question_title=answer.question.title if answer.question else None,
        author_id=answer.author_id,
        author_answers_count=author_answers_count,
        author_role=author.role if author else None,
        author_profile=author_profile,
        answer_text=answer.answer_text,
        code_example=answer.code_example,
        links=answer.links or [],
        expert_name=expert_name or _client_name(author),
        expert_rating=answer.expert_rating or 0.0,
        is_accepted=answer.is_accepted,
        created_at=answer.created_at,
    )


@router.get("/", response_model=QuestionListResponse)
def list_questions(
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    search: Optional[str] = None,
    sort_by: str = Query(
        "newest",
        pattern="^(newest|oldest|most-answered|least-answered)$",
    ),
    status_filter: Optional[str] = Query("published"),
    tags: Optional[List[str]] = Query(None),
) -> QuestionListResponse:
    query = (
        db.query(Question)
        .options(
            joinedload(Question.client).joinedload(User.expert_profile),
            joinedload(Question.answers),
        )
        .filter(Question.status.in_(PUBLIC_STATUSES))
    )

    if category:
        query = query.filter(Question.category == category)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    normalized_search = (search or "").strip()
    if normalized_search:
        search_pattern = f"%{normalized_search}%"
        query = query.filter(
            or_(
                Question.title.ilike(search_pattern),
                Question.description.ilike(search_pattern),
            )
        )
    if status_filter and status_filter.lower() != "all":
        normalized = status_filter.lower()
        if normalized != "published":
            query = query.filter(Question.status == normalized)

    if sort_by == "oldest":
        query = query.order_by(Question.created_at.asc(), Question.id.asc())
    elif sort_by in {"most-answered", "least-answered"}:
        answer_count = (
            select(func.count(Answer.id))
            .where(Answer.question_id == Question.id)
            .scalar_subquery()
        )
        count_order = (
            answer_count.desc()
            if sort_by == "most-answered"
            else answer_count.asc()
        )
        query = query.order_by(
            count_order, Question.created_at.desc(), Question.id.desc()
        )
    else:
        query = query.order_by(Question.created_at.desc(), Question.id.desc())

    if tags:
        normalized_tags = {tag.lower() for tag in tags if tag}
        questions = query.all()
        filtered = [
            question
            for question in questions
            if normalized_tags.issubset(
                {tag.lower() for tag in (question.tags or [])}
            )
        ]
        total = len(filtered)
        items = filtered[offset : offset + limit]
    else:
        total = query.order_by(None).count()
        items = query.offset(offset).limit(limit).all()

    return QuestionListResponse(
        total=total,
        items=[question_to_schema(question) for question in items],
    )


@router.post(
    "/",
    response_model=QuestionOut,
    status_code=status.HTTP_201_CREATED,
)
def create_question(
    payload: QuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> QuestionOut:
    tags = _clean_list(payload.tags)
    links = _clean_list(payload.links)

    if payload.code_link:
        if payload.code_link not in links:
            links.insert(0, payload.code_link)

    question = Question(
        title=payload.title,
        description=payload.description,
        code_example=payload.code_example,
        category=payload.category,
        subcategory=payload.subcategory,
        difficulty=payload.difficulty,
        tags=tags,
        links=links,
        deadline=payload.deadline,
        status=payload.status or "published",
        client_id=current_user.id,
    )

    db.add(question)
    db.commit()
    db.refresh(question)

    return question_to_schema(question)


@router.get("/{question_id}", response_model=QuestionOut)
def get_question(
    question_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> QuestionOut:
    question = (
        db.query(Question)
        .options(
            joinedload(Question.client).joinedload(User.expert_profile),
            joinedload(Question.answers),
        )
        .filter(Question.id == question_id)
        .first()
    )
    return question_to_schema(_require_visible_question(question, current_user))


@router.put("/{question_id}", response_model=QuestionOut)
def update_question(
    question_id: str,
    payload: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> QuestionOut:
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    if question.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own questions",
        )

    for field, value in payload.model_dump(exclude_unset=True).items():
        if field == "tags":
            question.tags = _clean_list(value)
        elif field == "links":
            question.links = _clean_list(value)
        elif field == "code_link" and value:
            links = question.links or []
            if value not in links:
                links.insert(0, value)
                question.links = links
        elif field == "code_example":
            question.code_example = value
        elif hasattr(question, field):
            setattr(question, field, value)

    db.add(question)
    db.commit()
    db.refresh(question)

    return question_to_schema(question)


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_question(
    question_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    question = (
        db.query(Question)
        .options(
            joinedload(Question.answers)
            .joinedload(Answer.author)
            .joinedload(User.expert_profile)
        )
        .filter(Question.id == question_id)
        .first()
    )
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    if question.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own questions",
        )

    # If the question had accepted answers, decrement those authors' resolved counts
    for answer in question.answers or []:
        if answer.is_accepted:
            _adjust_resolved_questions(answer.author, -1)

    # Ensure expert profiles exist for authors before adjustments
    for ans in question.answers or []:
        _ensure_expert_profile(ans.author, db)
    db.delete(question)
    db.commit()


@router.post("/{question_id}/submit", response_model=QuestionOut)
def publish_draft_question(
    question_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> QuestionOut:
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    if question.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only publish your own questions",
        )
    if question.status != "draft":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Only draft questions can be published",
        )
    question.status = "published"
    db.add(question)
    db.commit()
    db.refresh(question)
    return question_to_schema(question)


@router.get("/{question_id}/answers", response_model=List[AnswerOut])
def list_answers(
    question_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_current_user),
) -> List[AnswerOut]:
    question = (
        db.query(Question)
        .options(
            joinedload(Question.answers)
            .joinedload(Answer.author)
            .joinedload(User.expert_profile),
            joinedload(Question.answers)
            .joinedload(Answer.author)
            .joinedload(User.answers),
        )
        .filter(Question.id == question_id)
        .first()
    )
    _require_visible_question(question, current_user)
    return [answer_to_schema(answer) for answer in question.answers]


@router.post(
    "/{question_id}/answers",
    response_model=AnswerOut,
    status_code=status.HTTP_201_CREATED,
)
def create_answer(
    question_id: str,
    payload: AnswerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> AnswerOut:
    question = (
        db.query(Question)
        .options(joinedload(Question.client))
        .filter(Question.id == question_id)
        .first()
    )
    if not question:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question not found")
    if question.status not in PUBLIC_STATUSES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Answers are only available for published questions",
        )
    if question.client_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You cannot answer your own question",
        )
    if current_user.expert_profile is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Complete an expert profile before answering questions",
        )

    links = _clean_list(payload.links)
    answer = Answer(
        question_id=question.id,
        author_id=current_user.id,
        answer_text=payload.answer_text,
        code_example=payload.code_example,
        links=links,
        expert_name=_client_name(current_user),
        expert_rating=(
            current_user.expert_profile.average_rating
            if current_user.expert_profile
            else 0.0
        ),
    )

    db.add(answer)
    db.commit()
    db.refresh(answer)
    answer.question = question

    return answer_to_schema(answer)


@router.put("/{question_id}/answers/{answer_id}", response_model=AnswerOut)
def update_answer(
    question_id: str,
    answer_id: str,
    payload: AnswerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> AnswerOut:
    answer = (
        db.query(Answer)
        .filter(Answer.id == answer_id, Answer.question_id == question_id)
        .first()
    )
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found"
        )
    if answer.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own answers",
        )

    data = payload.model_dump(exclude_unset=True)
    if "answer_text" in data:
        answer.answer_text = data["answer_text"]
    if "code_example" in data:
        answer.code_example = data["code_example"]
    if "links" in data and data["links"] is not None:
        answer.links = data["links"]

    db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer_to_schema(answer)


@router.delete("/{question_id}/answers/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_answer(
    question_id: str,
    answer_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    answer = (
        db.query(Answer)
        .options(joinedload(Answer.author).joinedload(User.expert_profile))
        .filter(Answer.id == answer_id, Answer.question_id == question_id)
        .first()
    )
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found"
        )
    if answer.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own answers",
        )

    # If accepted, decrement author's resolved count
    if answer.is_accepted:
        _adjust_resolved_questions(answer.author, -1)

    # Update question acceptance state
    question = (
        db.query(Question)
        .options(joinedload(Question.answers))
        .filter(Question.id == question_id)
        .first()
    )

    if question:
        # remove from relationship to avoid re-attach of deleted instance
        if question.answers and answer in question.answers:
            question.answers.remove(answer)

        if question.accepted_answer_id == answer.id:
            question.accepted_answer_id = None
            # If there is another accepted answer, keep it; otherwise mark published
            replacement = next(
                (a for a in question.answers if getattr(a, "is_accepted", False)), None
            )
            if replacement:
                question.accepted_answer_id = replacement.id
                question.status = "resolved"
            else:
                question.status = "published"
        db.add(question)

    db.delete(answer)
    db.commit()


@router.post(
    "/{question_id}/answers/{answer_id}/verify",
    response_model=AnswerOut,
)
def verify_answer(
    question_id: str,
    answer_id: str,
    payload: AnswerModerationRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> AnswerOut:
    question = (
        db.query(Question)
        .options(joinedload(Question.client))
        .filter(Question.id == question_id)
        .first()
    )
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )
    if question.client_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only the question owner can verify answers",
        )

    answer = (
        db.query(Answer)
        .options(joinedload(Answer.author).joinedload(User.expert_profile))
        .filter(Answer.id == answer_id, Answer.question_id == question_id)
        .first()
    )
    if not answer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Answer not found"
        )

    is_marked_correct = payload.is_correct

    if is_marked_correct:
        _ensure_expert_profile(answer.author, db)
        other_accepted_answers = (
            db.query(Answer)
            .options(joinedload(Answer.author).joinedload(User.expert_profile))
            .filter(
                Answer.question_id == question_id,
                Answer.is_accepted.is_(True),
                Answer.id != answer.id,
            )
            .all()
        )
        for other in other_accepted_answers:
            other.is_accepted = False
            _adjust_resolved_questions(other.author, -1)
        if not answer.is_accepted:
            answer.is_accepted = True
            _adjust_resolved_questions(answer.author, 1)
        question.accepted_answer_id = answer.id
        question.status = "resolved"
    else:
        if answer.is_accepted:
            _adjust_resolved_questions(answer.author, -1)
        answer.is_accepted = False
        if question.accepted_answer_id == answer.id:
            replacement = (
                db.query(Answer)
                .filter(
                    Answer.question_id == question.id,
                    Answer.is_accepted.is_(True),
                    Answer.id != answer.id,
                )
                .first()
            )
            question.accepted_answer_id = replacement.id if replacement else None
        question.status = "resolved" if question.accepted_answer_id else "published"

    db.add(question)
    db.add(answer)
    db.commit()
    updated_answer = (
        db.query(Answer)
        .options(joinedload(Answer.author).joinedload(User.expert_profile))
        .filter(Answer.id == answer.id)
        .first()
    )
    if updated_answer:
        updated_answer.question = question
        return answer_to_schema(updated_answer)
    answer.question = question
    return answer_to_schema(answer)

