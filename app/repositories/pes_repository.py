import asyncio
from typing import Any

import httpx

from app.models.plan_data import PlanData
from app.repositories.interfaces.pes_repository_interface import (
    IPESRepository,
)


class PESRepository(IPESRepository):
    """Repository responsible for retrieving plan data from PES APIs."""

    def __init__(
        self,
        http_client: httpx.AsyncClient,
    ) -> None:
        self._http_client = http_client

    async def get_plan_data(
        self,
        plan_number: str,
        user_id: str,
    ) -> PlanData:

        (
            plan_information,
            eligibility,
            payroll,
            contribution,
            investment,
            vesting,
            loans,
            withdrawals,
            services,
            adp_features,
        ) = await asyncio.gather(
            self._get_plan_information(plan_number),
            self._get_eligibility(plan_number, user_id),
            self._get_payroll(plan_number, user_id),
            self._get_contribution(plan_number, user_id),
            self._get_investment(plan_number, user_id),
            self._get_vesting(plan_number, user_id),
            self._get_loans(plan_number, user_id),
            self._get_withdrawals(plan_number, user_id),
            self._get_services(plan_number, user_id),
            self._get_adp_features(plan_number),
        )

        return PlanData(
            plan_number=plan_number,
            user_id=user_id,
            data={
                "plan_information": plan_information,
                "eligibility": eligibility,
                "payroll": payroll,
                "contribution": contribution,
                "investment": investment,
                "vesting": vesting,
                "loans": loans,
                "withdrawals": withdrawals,
                "services": services,
                "adp_features": adp_features,
            },
        )

    async def _get_plan_information(
        self,
        plan_number: str,
    ) -> dict[str, Any]:
        # TODO: Call PES API
        return {}

    async def _get_eligibility(
        self,
        plan_number: str,
        user_id: str,
    ) -> dict[str, Any]:
        # TODO: Call PES API
        return {}

    async def _get_payroll(
        self,
        plan_number: str,
        user_id: str,
    ) -> dict[str, Any]:
        # TODO: Call PES API
        return {}

    async def _get_contribution(
        self,
        plan_number: str,
        user_id: str,
    ) -> dict[str, Any]:
        # TODO: Call PES API
        return {}

    async def _get_investment(
        self,
        plan_number: str,
        user_id: str,
    ) -> dict[str, Any]:
        # TODO: Call PES API
        return {}

    async def _get_vesting(
        self,
        plan_number: str,
        user_id: str,
    ) -> dict[str, Any]:
        # TODO: Call PES API
        return {}

    async def _get_loans(
        self,
        plan_number: str,
        user_id: str,
    ) -> dict[str, Any]:
        # TODO: Call PES API
        return {}

    async def _get_withdrawals(
        self,
        plan_number: str,
        user_id: str,
    ) -> dict[str, Any]:
        # TODO: Call PES API
        return {}

    async def _get_services(
        self,
        plan_number: str,
        user_id: str,
    ) -> dict[str, Any]:
        # TODO: Call PES API
        return {}

    async def _get_adp_features(
        self,
        plan_number: str,
    ) -> dict[str, Any]:
        # TODO: Call PES API
        return {}