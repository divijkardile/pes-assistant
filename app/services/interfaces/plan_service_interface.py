from abc import ABC, abstractmethod

from app.models.plan_context import PlanContext
from app.models.plan_data import PlanData


class IPlanService(ABC):

    @abstractmethod
    async def get_plan_data(
        self,
        plan_context: PlanContext,
    ) -> PlanData:
        raise NotImplementedError

    @abstractmethod
    async def refresh_plan_data(
        self,
        plan_context: PlanContext,
    ) -> PlanData:
        raise NotImplementedError