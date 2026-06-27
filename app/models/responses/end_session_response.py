from pydantic import BaseModel


class EndSessionResponse(BaseModel):
    """Response returned after ending a chat session."""

    message: str