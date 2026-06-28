from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "PES Assistant"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = False
    api_prefix: str = "/api/v1"

    # Retry
    retry_max_attempts: int = 2
    retry_initial_delay: float = 0.5
    retry_backoff_multiplier: float = 2.0

    # LLM
    llm_provider: str = "ollama"

    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_model: str = "llama3.2"
    ollama_embedding_model: str = "nomic-embed-text"

    # Bedrock
    aws_region: str = "us-east-1"
    bedrock_model: str = (
        "anthropic.claude-3-5-sonnet-20241022-v2:0"
    )

    bedrock_embedding_model: str = (
        "amazon.titan-embed-text-v2:0"
    )

    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_session_token: str | None = None

    #Open AI
    openai_api_key: str =""
    openai_model: str ="gpt-5.5"
    openai_embedding_model: str ="text-embedding-3-small"

    # Embeddings
    embedding_dimension: int = 768

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_api_key: str | None = None

    # Semantic Cache
    semantic_cache_enabled: bool = False
    semantic_cache_collection_name: str = "semantic_cache"
    semantic_cache_similarity_threshold: float = 0.95
    semantic_cache_ttl_minutes: int = 30

    # Documents
    document_path: str = "./documents"

    # Session
    session_timeout_minutes: int = 30

    # Agent Robustness (Timeout & Loop Prevention)
    agent_timeout_seconds: int = 30
    agent_max_iterations: int = 5
    tool_timeout_seconds: int = 15
    enable_loop_detection: bool = True
    loop_detection_threshold: int = 4  # Warn if same tool called > this many times

    # OAuth Configuration
    oauth_enabled: bool = False
    oauth_token_url: str | None = None
    oauth_scope: str | None = None  # e.g., "read write"

    # External API Endpoints (Placeholders)
    # Replace these with your actual API endpoints
    external_api_pes_base_url: str | None = None  # e.g., "https://api.pes.com"
    external_api_documents_base_url: str | None = None  # e.g., "https://api.documents.com"

    # Logging
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    return Settings() # type: ignore