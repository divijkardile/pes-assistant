from pydantic import BaseModel


class PlanContext(BaseModel):
    """Minimal context shared across the conversation."""

    plan_num: str
    user_id: str