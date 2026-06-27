import json
from typing import Any

from pydantic import BaseModel
from strands import tool

from app.models.agent_state import AgentState
from app.services.interfaces.plan_service_interface import (
    IPlanService,
)


class GetPlanDataTool:

    def __init__(
        self,
        plan_service: IPlanService,
    ) -> None:
        self._plan_service = plan_service

    @tool(
        name="get_plan_data",
        description="""
Retrieve structured retirement plan data for the current participant.

Use this tool whenever structured participant or plan
information is required.
""",
    )
    async def get_plan_data(
        self,
        state: AgentState,
    ) -> str:

        if state.plan_data is None:
            state.plan_data = await self._plan_service.get_plan_data(
                plan_context=state.plan_context,
            )

        plan_data = state.plan_data

        if isinstance(plan_data, BaseModel):
            return plan_data.model_dump_json(
                indent=2,
            )

        if isinstance(plan_data, (dict, list)):
            return json.dumps(
                plan_data,
                indent=2,
                default=str,
            )

        return str(plan_data)