import logging
from typing import Any, Optional

import httpx

from app.config.settings import get_settings
from app.exceptions.service_exception import ServiceException


logger = logging.getLogger(__name__)


class OAuthTokenManager:
    """Manages OAuth token retrieval and caching."""

    def __init__(self):
        self._cached_token: Optional[str] = None
        self._token_expiry: Optional[float] = None

    async def get_token(
        self,
        http_client: httpx.AsyncClient,
    ) -> str:
        """
        Get OAuth token. Returns cached token if available, otherwise fetches new one.
        
        Args:
            http_client: HTTPX async client for making requests
            
        Returns:
            OAuth access token
            
        Raises:
            ServiceException: If token retrieval fails
        """
        settings = get_settings()

        # Return cached token if still valid
        if self._cached_token:
            logger.debug("Using cached OAuth token")
            return self._cached_token

        if not settings.oauth_enabled:
            raise ServiceException(
                "OAuth is disabled. Enable it in settings to fetch tokens."
            )

        if not settings.oauth_token_url:
            raise ServiceException(
                "oauth_token_url is not configured in settings"
            )

        try:
            logger.info("Fetching OAuth token from: %s", settings.oauth_token_url)

            # OAuth request with scope only
            oauth_body = {}
            if settings.oauth_scope:
                oauth_body["scope"] = settings.oauth_scope

            response = await http_client.post(
                settings.oauth_token_url,
                json=oauth_body,
                timeout=10.0,
            )

            response.raise_for_status()
            token_response = response.json()

            self._cached_token = token_response.get("access_token")

            if not self._cached_token:
                raise ServiceException(
                    "No access_token in OAuth response"
                )

            logger.info("OAuth token retrieved successfully")
            return self._cached_token

        except httpx.RequestError as e:
            logger.error(f"OAuth token request failed: {str(e)}")
            raise ServiceException(
                f"Failed to get OAuth token: {str(e)}"
            )

        except httpx.HTTPStatusError as e:
            logger.error(
                f"OAuth token request returned status {e.response.status_code}: "
                f"{e.response.text}"
            )
            raise ServiceException(
                f"OAuth token request failed with status {e.response.status_code}"
            )

    def clear_cache(self) -> None:
        """Clear cached token."""
        self._cached_token = None
        self._token_expiry = None
        logger.debug("OAuth token cache cleared")


# Global token manager instance
_token_manager = OAuthTokenManager()


async def call_external_api(
    http_client: httpx.AsyncClient,
    endpoint: str,
    method: str = "GET",
    data: Optional[dict] = None,
    params: Optional[dict] = None,
    headers: Optional[dict[str, str]] = None,
) -> dict[str, Any]:
    """
    Call external API with OAuth authentication.
    
    Handles:
    - OAuth token retrieval if enabled
    - Authorization header injection
    - Custom headers support
    - Error handling and logging
    - Timeout management
    
    Args:
        http_client: HTTPX async client
        endpoint: Full API endpoint URL
        method: HTTP method (GET, POST, etc.)
        data: Request body data (for POST/PUT)
        params: Query parameters
        headers: Custom headers to include in request
        
    Returns:
        Parsed JSON response
        
    Raises:
        ServiceException: If API call fails
        
    Example:
        response = await call_external_api(
            http_client,
            "https://api.example.com/plans",
            method="GET",
            headers={"user_id": "user123", "plan_number": "12345"}
        )
    """
    settings = get_settings()
    request_headers = headers or {}

    # Add OAuth token if enabled
    if settings.oauth_enabled:
        try:
            token = await _token_manager.get_token(http_client)
            request_headers["Authorization"] = f"Bearer {token}"
            logger.debug("Added OAuth token to request headers")

        except ServiceException as e:
            logger.error(f"Failed to add OAuth token: {str(e)}")
            raise

    try:
        logger.info(
            f"[API] {method} request to: {endpoint}",
        )

        response = await http_client.request(
            method=method,
            url=endpoint,
            json=data if method in ["POST", "PUT", "PATCH"] else None,
            params=params,
            headers=request_headers,
            timeout=30.0,
        )

        response.raise_for_status()
        result = response.json()

        logger.info(
            f"[API] {method} {endpoint} - Status: {response.status_code}",
        )

        return result

    except httpx.RequestError as e:
        logger.error(f"API request failed: {str(e)}")
        raise ServiceException(
            f"API request failed: {str(e)}"
        )

    except httpx.HTTPStatusError as e:
        logger.error(
            f"API returned status {e.response.status_code}: "
            f"{e.response.text}"
        )
        raise ServiceException(
            f"API request failed with status {e.response.status_code}"
        )

    except ValueError as e:
        logger.error(f"Failed to parse API response: {str(e)}")
        raise ServiceException(
            f"Invalid API response format: {str(e)}"
        )


def get_token_manager() -> OAuthTokenManager:
    """Get the global OAuth token manager instance."""
    return _token_manager
