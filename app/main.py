from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.config.settings import get_settings
from app.dependencies import get_http_client

from app.config.logging import configure_logging
from app.config.settings import get_settings

settings = get_settings()

configure_logging(settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application startup and shutdown events.
    """

    yield

    http_client = get_http_client()
    await http_client.aclose()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(
    chat_router,
    prefix=settings.api_prefix,
)


@app.get(
    "/health",
    tags=["Health"],
)
async def health() -> dict[str, str]:
    return {
        "status": "UP",
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }