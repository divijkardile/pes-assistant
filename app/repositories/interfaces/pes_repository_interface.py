from abc import ABC, abstractmethod

from app.models.plan_data import PlanData


class IPESRepository(ABC):
    """Repository responsible for retrieving plan data from PES."""

    @abstractmethod
    async def get_plan_data(
        self,
        plan_number: str,
        user_id: str,
    ) -> PlanData:
        raise NotImplementedError