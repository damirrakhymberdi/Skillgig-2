import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import relationship

from ..database import Base


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    __table_args__ = (
        Index(
            "ix_chat_messages_conversation",
            "question_id",
            "sender_id",
            "recipient_id",
            "created_at",
        ),
    )

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    question_id = Column(
        String, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )
    sender_id = Column(String, ForeignKey("users.id"), nullable=False)
    recipient_id = Column(String, ForeignKey("users.id"), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    question = relationship("Question", back_populates="chat_messages")
