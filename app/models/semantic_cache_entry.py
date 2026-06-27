from datetime import UTC, datetime

from pydantic import BaseModel, Field


class SemanticCacheEntry(BaseModel):
    """
    Represents a semantic cache entry.
    """

    id: str

    plan_num: str

    user_id: str

    question: str

    embedding: list[float]

    response: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )