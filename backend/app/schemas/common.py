from typing import Any, Callable
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict


def to_camel(string: str) -> str:
    parts = string.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])


class CamelModel(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
        alias_generator=to_camel,
    )


class Message(CamelModel):
    detail: str


def validate_external_web_url(value: str) -> str:
    value = value.strip()
    parsed = urlsplit(value)
    if (
        parsed.scheme.lower() not in {"http", "https"}
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
    ):
        raise ValueError("Links must be absolute HTTP or HTTPS URLs")
    return value

