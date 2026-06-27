from pydantic import BaseModel


class StartSessionRequest(BaseModel):
    """Request to start a new chat session."""

    user_id: str
    plan_number: str