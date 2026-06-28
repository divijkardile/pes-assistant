import asyncio
import logging
from typing import Any

import httpx

from app.config.settings import get_settings
from app.gateway.api_helper import call_external_api
from app.models.plan_data import PlanData
from app.repositories.interfaces.pes_repository_interface import (
    IPESRepository,
)
from app.utils.execution_timer import execution_timer

logger = logging.getLogger(__name__)


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

    @execution_timer
    async def _get_plan_information(
        self,
        plan_number: str,
    ) -> dict[str, Any]:
        """
        Retrieve plan information from PES API.
        
        API Call:
        Endpoint: {external_api_pes_base_url}/information
        Method: GET
        Headers: plan_number, Authorization (OAuth if enabled)
        Auth: OAuth (if enabled)
        """
        settings = get_settings()
        
        if not settings.external_api_pes_base_url:
            logger.warning("external_api_pes_base_url not configured")
            return {}
        
        try:
            endpoint = f"{settings.external_api_pes_base_url}/information"
            response = await call_external_api(
                self._http_client,
                endpoint=endpoint,
                method="GET",
                headers={"plan_number": plan_number},
            )
            return response
        except Exception as e:
            logger.error(
                f"Failed to get plan information for {plan_number}: {str(e)}"
            )
            return {}

    @execution_timer
    async def _get_eligibility(
        self,
        plan_number: str,
        user_id: str,
    ) -> dict[str, Any]:
        """
        Retrieve eligibility information from PES API.
        
        API Call:
        Endpoint: {external_api_pes_base_url}/eligibility
        Method: GET
        Headers: plan_number, user_id, Authorization (OAuth if enabled)
        """
        settings = get_settings()
        
        if not settings.external_api_pes_base_url:
            logger.warning("external_api_pes_base_url not configured")
            return {}
        
        try:
            endpoint = f"{settings.external_api_pes_base_url}/eligibility"
            response = await call_external_api(
                self._http_client,
                endpoint=endpoint,
                method="GET",
                headers={"plan_number": plan_number, "user_id": user_id},
            )
            return response
        except Exception as e:
            logger.error(
                f"Failed to get eligibility for {plan_number}/{user_id}: "
                f"{str(e)}"
            )
            return {}

    @execution_timer
    async def _get_payroll(
        self,
        plan_number: str,
        user_id: str,
    ) -> dict[str, Any]:
        """
        Retrieve payroll information from PES API.
        
        API Call:
        Endpoint: {external_api_pes_base_url}/payroll
        Method: GET
        Headers: plan_number, user_id, Authorization (OAuth if enabled)
        """
        settings = get_settings()
        
        if not settings.external_api_pes_base_url:
            logger.warning("external_api_pes_base_url not configured")
            return {}
        
        try:
            endpoint = f"{settings.external_api_pes_base_url}/payroll"
            response = await call_external_api(
                self._http_client,
                endpoint=endpoint,
                method="GET",
                headers={"plan_number": plan_number, "user_id": user_id},
            )
            return response
        except Exception as e:
            logger.error(
                f"Failed to get payroll for {plan_number}/{user_id}: "
                f"{str(e)}"
            )
            return {}

    @execution_timer
    async def _get_contribution(
        self,
        plan_number: str,
        user_id: str,
    ) -> dict[str, Any]:
        """
        Retrieve contribution information from PES API.
        
        API Call:
        Endpoint: {external_api_pes_base_url}/contribution
        Method: GET
        Headers: plan_number, user_id, Authorization (OAuth if enabled)
        """
        settings = get_settings()
        
        if not settings.external_api_pes_base_url:
            logger.warning("external_api_pes_base_url not configured")
            return {}
        
        try:
            endpoint = f"{settings.external_api_pes_base_url}/contribution"
            response = await call_external_api(
                self._http_client,
                endpoint=endpoint,
                method="GET",
                headers={"plan_number": plan_number, "user_id": user_id},
            )
            return response
        except Exception as e:
            logger.error(
                f"Failed to get contribution for {plan_number}/{user_id}: "
                f"{str(e)}"
            )
            return {}

    @execution_timer
    async def _get_investment(
        self,
        plan_number: str,
        user_id: str,
    ) -> dict[str, Any]:
        """
        Retrieve investment information from PES API.
        
        API Call:
        Endpoint: {external_api_pes_base_url}/investment
        Method: GET
        Headers: plan_number, user_id, Authorization (OAuth if enabled)
        """
        settings = get_settings()
        
        if not settings.external_api_pes_base_url:
            logger.warning("external_api_pes_base_url not configured")
            return {}
        
        try:
            endpoint = f"{settings.external_api_pes_base_url}/investment"
            response = await call_external_api(
                self._http_client,
                endpoint=endpoint,
                method="GET",
                headers={"plan_number": plan_number, "user_id": user_id},
            )
            return response
        except Exception as e:
            logger.error(
                f"Failed to get investment for {plan_number}/{user_id}: "
                f"{str(e)}"
            )
            return {}

    @execution_timer
    async def _get_vesting(
        self,
        plan_number: str,
        user_id: str,
    ) -> dict[str, Any]:
        """
        Retrieve vesting information from PES API.
        
        API Call:
        Endpoint: {external_api_pes_base_url}/vesting
        Method: GET
        Headers: plan_number, user_id, Authorization (OAuth if enabled)
        """
        settings = get_settings()
        
        if not settings.external_api_pes_base_url:
            logger.warning("external_api_pes_base_url not configured")
            return {}
        
        try:
            endpoint = f"{settings.external_api_pes_base_url}/vesting"
            response = await call_external_api(
                self._http_client,
                endpoint=endpoint,
                method="GET",
                headers={"plan_number": plan_number, "user_id": user_id},
            )
            return response
        except Exception as e:
            logger.error(
                f"Failed to get vesting for {plan_number}/{user_id}: "
                f"{str(e)}"
            )
            return {}

    @execution_timer
    async def _get_loans(
        self,
        plan_number: str,
        user_id: str,
    ) -> dict[str, Any]:
        """
        Retrieve loans information from PES API.
        
        API Call:
        Endpoint: {external_api_pes_base_url}/loans
        Method: GET
        Headers: plan_number, user_id, Authorization (OAuth if enabled)
        """
        settings = get_settings()
        
        if not settings.external_api_pes_base_url:
            logger.warning("external_api_pes_base_url not configured")
            return {}
        
        try:
            endpoint = f"{settings.external_api_pes_base_url}/loans"
            response = await call_external_api(
                self._http_client,
                endpoint=endpoint,
                method="GET",
                headers={"plan_number": plan_number, "user_id": user_id},
            )
            return response
        except Exception as e:
            logger.error(
                f"Failed to get loans for {plan_number}/{user_id}: "
                f"{str(e)}"
            )
            return {}

    @execution_timer
    async def _get_withdrawals(
        self,
        plan_number: str,
        user_id: str,
    ) -> dict[str, Any]:
        """
        Retrieve withdrawals information from PES API.
        
        API Call:
        Endpoint: {external_api_pes_base_url}/withdrawals
        Method: GET
        Headers: plan_number, user_id, Authorization (OAuth if enabled)
        """
        settings = get_settings()
        
        if not settings.external_api_pes_base_url:
            logger.warning("external_api_pes_base_url not configured")
            return {}
        
        try:
            endpoint = f"{settings.external_api_pes_base_url}/withdrawals"
            response = await call_external_api(
                self._http_client,
                endpoint=endpoint,
                method="GET",
                headers={"plan_number": plan_number, "user_id": user_id},
            )
            return response
        except Exception as e:
            logger.error(
                f"Failed to get withdrawals for {plan_number}/{user_id}: "
                f"{str(e)}"
            )
            return {}

    @execution_timer
    async def _get_services(
        self,
        plan_number: str,
        user_id: str,
    ) -> dict[str, Any]:
        """
        Retrieve services information from PES API.
        
        API Call:
        Endpoint: {external_api_pes_base_url}/services
        Method: GET
        Headers: plan_number, user_id, Authorization (OAuth if enabled)
        """
        settings = get_settings()
        
        if not settings.external_api_pes_base_url:
            logger.warning("external_api_pes_base_url not configured")
            return {}
        
        try:
            endpoint = f"{settings.external_api_pes_base_url}/services"
            response = await call_external_api(
                self._http_client,
                endpoint=endpoint,
                method="GET",
                headers={"plan_number": plan_number, "user_id": user_id},
            )
            return response
        except Exception as e:
            logger.error(
                f"Failed to get services for {plan_number}/{user_id}: "
                f"{str(e)}"
            )
            return {}

    @execution_timer
    async def _get_adp_features(
        self,
        plan_number: str,
    ) -> dict[str, Any]:
        """
        Retrieve ADP features from PES API.
        
        API Call:
        Endpoint: {external_api_pes_base_url}/adp-features
        Method: GET
        Headers: plan_number, Authorization (OAuth if enabled)
        """
        settings = get_settings()
        
        if not settings.external_api_pes_base_url:
            logger.warning("external_api_pes_base_url not configured")
            return {}
        
        try:
            endpoint = f"{settings.external_api_pes_base_url}/adp-features"
            response = await call_external_api(
                self._http_client,
                endpoint=endpoint,
                method="GET",
                headers={"plan_number": plan_number},
            )
            return response
        except Exception as e:
            logger.error(
                f"Failed to get ADP features for {plan_number}: {str(e)}"
            )
            return {}