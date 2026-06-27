from pydantic import BaseModel


class ChatRequest(BaseModel):
    """Request to send a message to the assistant."""

    session_id: str
    message: str