from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field

from app.config.constants import Roles


class ChatMessage(BaseModel):
    """Represents a single message in a conversation."""

    message_id: str = Field(default_factory=lambda: str(uuid4()))
    role: str = Field(..., examples=[Roles.USER, Roles.ASSISTANT, Roles.SYSTEM])
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)