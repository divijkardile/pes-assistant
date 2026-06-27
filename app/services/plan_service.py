from app.models.plan_context import PlanContext
from app.models.plan_data import PlanData
from app.repositories.interfaces.pes_repository_interface import (
    IPESRepository,
)
from app.services.interfaces.plan_service_interface import IPlanService


class PlanAssistantService(IPlanService):
    """Service responsible for loading plan data."""

    def __init__(
        self,
        pes_repository: IPESRepository,
    ) -> None:
        self._pes_repository = pes_repository

    async def get_plan_data(
        self,
        plan_context: PlanContext,
    ) -> PlanData:
        return await self._pes_repository.get_plan_data(
            plan_number=plan_context.plan_num,
            user_id=plan_context.user_id,
        )

    async def refresh_plan_data(
        self,
        plan_context: PlanContext,
    ) -> PlanData:
        return await self.get_plan_data(plan_context)