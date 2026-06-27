from pydantic import BaseModel


class EndSessionRequest(BaseModel):
    """Request to end an existing chat session."""

    session_id: str