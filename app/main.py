# app/main.py

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.chat import router as chat_router
from app.config.logging import configure_logging
from app.config.settings import get_settings
from app.qdrant.qdrant_initializer import (
    initialize_qdrant,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    configure_logging(
        settings.log_level,
    )

    if settings.semantic_cache_enabled:
        await initialize_qdrant()

    yield


app = FastAPI(
    title="PES Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(
    chat_router,
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {
        "status": "healthy",
    }