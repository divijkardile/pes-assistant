from pydantic import BaseModel

class ChatResponse(BaseModel):
    """Assistant response."""
    session_id: str
    response: str