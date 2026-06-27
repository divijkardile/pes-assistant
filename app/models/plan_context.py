from pydantic import BaseModel


class PlanContext(BaseModel):
    """Minimal context shared across the conversation."""

    plan_number: str
    user_id: str