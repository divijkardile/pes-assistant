from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ------------------------------------------------------------------
    # Application
    # ------------------------------------------------------------------

    app_name: str = "PES Assistant"

    app_version: str = "1.0.0"

    environment: str = Field(
        default="development",
    )

    debug: bool = Field(
        default=False,
    )

    api_prefix: str = Field(
        default="/api/v1",
    )

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    log_level: str = Field(
        default="INFO",
    )

    # ------------------------------------------------------------------
    # Ollama
    # ------------------------------------------------------------------

    ollama_host: str = Field(
    default="http://localhost:11434",
    )

    ollama_model: str = Field(
        default="qwen3:8b",
    )

    # ------------------------------------------------------------------
    # Documents
    # ------------------------------------------------------------------

    document_path: str = Field(
        default="./documents",
    )

    # ------------------------------------------------------------------
    # Session
    # ------------------------------------------------------------------

    session_timeout_minutes: int = Field(
        default=30,
    )


@lru_cache
def get_settings() -> Settings:
    """Returns a cached application settings instance."""
    return Settings()