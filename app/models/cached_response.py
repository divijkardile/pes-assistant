from datetime import UTC, datetime

from pydantic import BaseModel, Field


class CachedResponse(BaseModel):
    """
    Represents a cached AI response.
    """

    question_hash: str

    response: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )