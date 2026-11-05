from datetime import datetime
from typing import List, Literal, Optional

from pydantic import ConfigDict, Field, field_validator

from .common import CamelModel, validate_external_web_url
from .user import ExpertProfilePublic


class QuestionBase(CamelModel):
    title: str = Field(..., max_length=255)
    description: str
    code_example: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    difficulty: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    links: List[str] = Field(default_factory=list)
    code_link: Optional[str] = None
    deadline: Optional[datetime] = None
    status: str = Field(default="draft")


class QuestionCreate(QuestionBase):
    status: Literal["draft", "published"] = "draft"

    @field_validator("links")
    @classmethod
    def validate_links(cls, values: List[str]) -> List[str]:
        return [validate_external_web_url(value) for value in values]

    @field_validator("code_link")
    @classmethod
    def validate_code_link(cls, value: Optional[str]) -> Optional[str]:
        return validate_external_web_url(value) if value else value


class QuestionUpdate(CamelModel):
    model_config = ConfigDict(extra="forbid")

    title: Optional[str] = None
    description: Optional[str] = None
    code_example: Optional[str] = None
    category: Optional[str] = None
    subcategory: Optional[str] = None
    difficulty: Optional[str] = None
    tags: Optional[List[str]] = None
    links: Optional[List[str]] = None
    code_link: Optional[str] = None
    deadline: Optional[datetime] = None
    @field_validator("links")
    @classmethod
    def validate_links(cls, values: Optional[List[str]]) -> Optional[List[str]]:
        return (
            [validate_external_web_url(value) for value in values]
            if values is not None
            else None
        )

    @field_validator("code_link")
    @classmethod
    def validate_code_link(cls, value: Optional[str]) -> Optional[str]:
        return validate_external_web_url(value) if value else value


class QuestionOut(QuestionBase):
    id: str
    client_id: str
    client_name: str
    client_role: Optional[str] = None
    client_profile: Optional[ExpertProfilePublic] = None
    answers_count: int = 0
    is_solved: bool = False
    accepted_answer_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class QuestionListResponse(CamelModel):
    total: int
    items: List[QuestionOut]
