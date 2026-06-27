from pydantic import BaseModel


class StartSessionResponse(BaseModel):
    """Response returned after creating a chat session."""

    session_id: str
    correlation_id: str
    message: str