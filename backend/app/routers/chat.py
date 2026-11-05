from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session, joinedload

from ..database import get_db
from ..deps import get_current_active_user
from ..models import ChatMessage, Question, User
from ..schemas.chat import ChatMessageCreate, ChatMessageOut

router = APIRouter(prefix="/chat", tags=["chat"])


def _validate_conversation(
    db: Session, question_id: str, partner_id: str, current_user: User
) -> None:
    question = (
        db.query(Question)
        .options(joinedload(Question.answers))
        .filter(Question.id == question_id)
        .first()
    )
    if not question:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )

    participants = {question.client_id}
    participants.update(answer.author_id for answer in question.answers or [])
    if (
        partner_id == current_user.id
        or current_user.id not in participants
        or partner_id not in participants
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chat is available only to people participating in this question",
        )


@router.get(
    "/questions/{question_id}/messages",
    response_model=List[ChatMessageOut],
)
def list_chat_messages(
    question_id: str,
    partner_id: str,
    limit: int = Query(100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> List[ChatMessageOut]:
    _validate_conversation(db, question_id, partner_id, current_user)
    messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.question_id == question_id,
            or_(
                and_(
                    ChatMessage.sender_id == current_user.id,
                    ChatMessage.recipient_id == partner_id,
                ),
                and_(
                    ChatMessage.sender_id == partner_id,
                    ChatMessage.recipient_id == current_user.id,
                ),
            ),
        )
        .order_by(ChatMessage.created_at.desc())
        .limit(limit)
        .all()
    )
    messages.reverse()
    return [
        ChatMessageOut.model_validate(message, from_attributes=True)
        for message in messages
    ]


@router.post(
    "/questions/{question_id}/messages",
    response_model=ChatMessageOut,
    status_code=status.HTTP_201_CREATED,
)
def create_chat_message(
    question_id: str,
    payload: ChatMessageCreate,
    partner_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ChatMessageOut:
    _validate_conversation(db, question_id, partner_id, current_user)
    message_text = payload.text.strip()
    if not message_text:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Message cannot be empty",
        )

    message = ChatMessage(
        question_id=question_id,
        sender_id=current_user.id,
        recipient_id=partner_id,
        text=message_text,
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return ChatMessageOut.model_validate(message, from_attributes=True)
