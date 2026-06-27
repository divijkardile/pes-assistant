from datetime import UTC, datetime

from pydantic import BaseModel, Field

from app.config.constants import Roles


class ChatMessage(BaseModel):
    """
    Represents a single message in the conversation.
    """

    role: str = Field(
        description="user | assistant | system",
    )

    content: str

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
    )

    @classmethod
    def user(
        cls,
        content: str,
    ) -> "ChatMessage":
        return cls(
            role=Roles.USER,
            content=content,
        )

    @classmethod
    def assistant(
        cls,
        content: str,
    ) -> "ChatMessage":
        return cls(
            role=Roles.ASSISTANT,
            content=content,
        )

    @classmethod
    def system(
        cls,
        content: str,
    ) -> "ChatMessage":
        return cls(
            role=Roles.SYSTEM,
            content=content,
        )