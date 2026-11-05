import uuid
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String, Text, JSON
from sqlalchemy.orm import relationship

from ..database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    subcategory = Column(String(100), nullable=True)
    difficulty = Column(String(50), nullable=True)
    tags = Column(JSON, default=list)
    links = Column(JSON, default=list)
    code_example = Column(Text, nullable=True)
    deadline = Column(DateTime, nullable=True)
    status = Column(String(50), default="draft", nullable=False)
    client_id = Column(String, ForeignKey("users.id"), nullable=False)
    accepted_answer_id = Column(String, ForeignKey("answers.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True
    )

    client = relationship("User", back_populates="questions")
    answers = relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete-orphan",
        foreign_keys="Answer.question_id",
    )
    chat_messages = relationship(
        "ChatMessage",
        back_populates="question",
        cascade="all, delete-orphan",
    )


class Answer(Base):
    __tablename__ = "answers"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    question_id = Column(String, ForeignKey("questions.id"), nullable=False)
    author_id = Column(String, ForeignKey("users.id"), nullable=False)
    answer_text = Column(Text, nullable=False)
    code_example = Column(Text, nullable=True)
    links = Column(JSON, default=list)
    expert_name = Column(String(255), nullable=True)
    expert_rating = Column(Float, nullable=True)
    is_accepted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    question = relationship(
        "Question",
        back_populates="answers",
        foreign_keys=[question_id],
    )
    author = relationship("User", back_populates="answers")

