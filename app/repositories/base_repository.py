from httpx import AsyncClient


class BaseRepository:
    """Base class for all repositories."""

    def __init__(self, http_client: AsyncClient) -> None:
        self._http_client = http_client