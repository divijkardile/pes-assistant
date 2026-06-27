from datetime import UTC, datetime

from pydantic import BaseModel, Field


class ConversationSummary(BaseModel):
    """
    Stores the running summary of a conversation.
    """

    summary: str = ""

    summarized_message_count: int = 0

    last_updated: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )