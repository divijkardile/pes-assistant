import logging
from functools import lru_cache

import httpx

from app.agents.data.data_agent import DataAgent
from app.agents.document.document_agent import DocumentAgent
from app.agents.memory.conversation_summary_agent import (
    ConversationSummaryAgent,
)
from app.agents.orchestrator.orchestrator_agent import (
    OrchestratorAgent,
)
from app.config.settings import get_settings
from app.gateway.ai_gateway import AIGateway
from app.gateway.retry_policy import RetryPolicy
from app.llm.embedding_provider_factory import (
    EmbeddingProviderFactory,
)
from app.llm.interfaces.embedding_provider import (
    EmbeddingProvider,
)
from app.llm.interfaces.llm_provider import LLMProvider
from app.llm.provider_factory import ProviderFactory
from app.repositories.document_repository import (
    DocumentRepository,
)
from app.repositories.pes_repository import (
    PESRepository,
)
from app.repositories.interfaces.semantic_cache_repository_interface import (
    ISemanticCacheRepository,
)
from app.repositories.in_memory_vector_repository import (
    InMemoryVectorRepository,
)
from app.repositories.qdrant_semantic_cache_repository import (
    QdrantSemanticCacheRepository,
)
from app.qdrant.collections import (
    QdrantCollection,
)
from app.qdrant.qdrant_client_factory import (
    get_qdrant_client,
)
from app.services.chat_service import ChatService
from app.services.conversation_memory_service import (
    ConversationMemoryService,
)
from app.services.document_service import DocumentService
from app.services.interfaces.session_manager_interface import (
    ISessionManager,
)
from app.services.plan_service import (
    PlanAssistantService,
)
from app.services.semantic_cache_service import (
    SemanticCacheService,
)
from app.services.session_manager import (
    SessionManager,
)
from app.tools.agent_tools import (
    create_data_agent_tool,
    create_document_agent_tool,
)
from app.tools.get_plan_data_tool import (
    GetPlanDataTool,
)
from app.tools.search_documents_tool import (
    SearchDocumentsTool,
)

settings = get_settings()

# ------------------------------------------------------------------
# Logger
# ------------------------------------------------------------------

logger = logging.getLogger("PESAssistant")

# ------------------------------------------------------------------
# LLM Provider
# ------------------------------------------------------------------


@lru_cache
def get_llm_provider() -> LLMProvider:
    return ProviderFactory.get_provider()


@lru_cache
def get_embedding_provider() -> EmbeddingProvider:
    return EmbeddingProviderFactory.get_provider()


llm_provider = get_llm_provider()

# ------------------------------------------------------------------
# HTTP Client
# ------------------------------------------------------------------

http_client = httpx.AsyncClient()

# ------------------------------------------------------------------
# Repositories
# ------------------------------------------------------------------

pes_repository = PESRepository(
    http_client=http_client,
)

document_repository = DocumentRepository(
    http_client=http_client,
)

# ------------------------------------------------------------------
# Semantic Cache Repository
# ------------------------------------------------------------------

if settings.semantic_cache_enabled:

    semantic_cache_repository: ISemanticCacheRepository = (
        QdrantSemanticCacheRepository(
            client=get_qdrant_client(),
            collection_name=QdrantCollection.SEMANTIC_CACHE,
        )
    )

else:

    semantic_cache_repository = (
        InMemoryVectorRepository(
            ttl_minutes=settings.semantic_cache_ttl_minutes,
        )
    )

# ------------------------------------------------------------------
# Semantic Cache Service
# ------------------------------------------------------------------

semantic_cache_service = SemanticCacheService(
    embedding_provider=get_embedding_provider(),
    vector_repository=semantic_cache_repository,
    similarity_threshold=settings.semantic_cache_similarity_threshold,
)

# ------------------------------------------------------------------
# Services
# ------------------------------------------------------------------

plan_service = PlanAssistantService(
    pes_repository=pes_repository,
)

document_service = DocumentService(
    document_repository=document_repository,
)

session_manager = SessionManager(
    session_timeout_minutes=settings.session_timeout_minutes,
)

# ------------------------------------------------------------------
# Internal Tools
# ------------------------------------------------------------------

get_plan_data_tool = GetPlanDataTool(
    plan_service=plan_service,
)

search_documents_tool = SearchDocumentsTool(
    document_service=document_service,
)

# ------------------------------------------------------------------
# Specialist Agents
# ------------------------------------------------------------------

data_agent = DataAgent(
    logger=logging.getLogger(DataAgent.__name__),
    llm_provider=llm_provider,
    get_plan_data_tool=get_plan_data_tool,
)

document_agent = DocumentAgent(
    logger=logging.getLogger(DocumentAgent.__name__),
    llm_provider=llm_provider,
    search_documents_tool=search_documents_tool,
)

summary_agent = ConversationSummaryAgent(
    logger=logging.getLogger(
        ConversationSummaryAgent.__name__,
    ),
    llm_provider=llm_provider,
)

# ------------------------------------------------------------------
# Conversation Memory
# ------------------------------------------------------------------

conversation_memory_service = ConversationMemoryService(
    summary_agent=summary_agent,
)

# ------------------------------------------------------------------
# Orchestrator Tools
# ------------------------------------------------------------------

data_agent_tool = create_data_agent_tool(
    data_agent=data_agent,
)

document_agent_tool = create_document_agent_tool(
    document_agent=document_agent,
)

# ------------------------------------------------------------------
# Orchestrator Agent
# ------------------------------------------------------------------

orchestrator_agent = OrchestratorAgent(
    logger=logging.getLogger(
        OrchestratorAgent.__name__,
    ),
    llm_provider=llm_provider,
    data_agent_tool=data_agent_tool,
    document_agent_tool=document_agent_tool,
)

# ------------------------------------------------------------------
# Chat Service
# ------------------------------------------------------------------

chat_service = ChatService(
    session_manager=session_manager,
    orchestrator_agent=orchestrator_agent,
    conversation_memory_service=conversation_memory_service,
    semantic_cache_service=semantic_cache_service,
)

# ------------------------------------------------------------------
# AI Gateway
# ------------------------------------------------------------------

ai_gateway = AIGateway(
    chat_service=chat_service,
    session_manager=session_manager,
    retry_policy=RetryPolicy(
        max_retries=settings.retry_max_attempts,
        initial_delay=settings.retry_initial_delay,
        backoff_multiplier=settings.retry_backoff_multiplier,
    ),
)

# ------------------------------------------------------------------
# FastAPI Dependencies
# ------------------------------------------------------------------


def get_chat_service() -> ChatService:
    return chat_service


def get_ai_gateway() -> AIGateway:
    return ai_gateway


def get_session_manager() -> ISessionManager:
    return session_manager


def get_http_client() -> httpx.AsyncClient:
    return http_client