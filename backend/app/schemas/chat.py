from datetime import datetime

from pydantic import Field

from .common import CamelModel


class ChatMessageCreate(CamelModel):
    text: str = Field(..., min_length=1, max_length=5000)


class ChatMessageOut(CamelModel):
    id: str
    question_id: str
    sender_id: str
    recipient_id: str
    text: str
    created_at: datetime
