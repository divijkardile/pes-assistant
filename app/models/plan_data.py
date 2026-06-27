from typing import Any

from pydantic import BaseModel, Field


class PlanData(BaseModel):
    """Aggregated plan data retrieved from PES."""

    plan_number: str
    user_id: str

    data: dict[str, Any] = Field(default_factory=dict)