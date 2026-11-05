from datetime import datetime
from typing import List, Literal, Optional

from pydantic import EmailStr, Field, field_validator

from .common import CamelModel, validate_external_web_url


class ExpertProfileBase(CamelModel):
    full_name: Optional[str] = None
    bio: Optional[str] = None
    primary_role: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    portfolio_url: Optional[str] = None
    experience_years: int = 0


class ExpertProfilePublic(ExpertProfileBase):
    average_rating: float = 0.0
    resolved_questions: int = 0


class ExpertProfileUpdate(ExpertProfileBase):
    @field_validator("github_url", "linkedin_url", "portfolio_url")
    @classmethod
    def validate_profile_links(cls, value: Optional[str]) -> Optional[str]:
        return validate_external_web_url(value) if value and value.strip() else value


class UserBase(CamelModel):
    id: str
    email: EmailStr
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str


class UserPublic(UserBase):
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    expert_profile: Optional[ExpertProfilePublic] = None
    answers_count: int = 0


class UserDirectoryProfile(CamelModel):
    id: str
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str
    is_active: Optional[bool] = None
    created_at: Optional[datetime] = None
    expert_profile: Optional[ExpertProfilePublic] = None
    answers_count: int = 0


class UserCreate(CamelModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    role: Literal["client", "expert"] = "client"
    username: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=30,
        pattern=r"^[A-Za-z0-9_]+$",
    )
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @field_validator("password")
    @classmethod
    def validate_password_byte_length(cls, value: str) -> str:
        if len(value.encode("utf-8")) > 72:
            raise ValueError("Password must not exceed 72 UTF-8 bytes")
        return value


class UserProfileResponse(UserPublic):
    pass

