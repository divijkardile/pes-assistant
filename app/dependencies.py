import logging

import httpx

from app.agents.data.data_agent import DataAgent
from app.agents.document.document_agent import DocumentAgent
from app.agents.orchestrator.orchestrator_agent import OrchestratorAgent
from app.config.settings import get_settings
from app.repositories.document_repository import DocumentRepository
from app.repositories.pes_repository import PESRepository
from app.services.chat_service import ChatService
from app.services.document_service import DocumentService
from app.services.plan_service import PlanAssistantService
from app.services.session_manager import SessionManager
from app.tools.agent_tools import (
    create_data_agent_tool,
    create_document_agent_tool,
)
from app.tools.get_plan_data_tool import GetPlanDataTool
from app.tools.search_documents_tool import SearchDocumentsTool

settings = get_settings()

# ------------------------------------------------------------------
# Logger
# ------------------------------------------------------------------

logger = logging.getLogger("PESAssistant")

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
    ollama_host=settings.ollama_host,
    model_id=settings.ollama_model,
    get_plan_data_tool=get_plan_data_tool,
)

document_agent = DocumentAgent(
    logger=logging.getLogger(DocumentAgent.__name__),
    ollama_host=settings.ollama_host,
    model_id=settings.ollama_model,
    search_documents_tool=search_documents_tool,
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
    logger=logging.getLogger(OrchestratorAgent.__name__),
    ollama_host=settings.ollama_host,
    model_id=settings.ollama_model,
    data_agent_tool=data_agent_tool,
    document_agent_tool=document_agent_tool,
)

# ------------------------------------------------------------------
# Chat Service
# ------------------------------------------------------------------

chat_service = ChatService(
    session_manager=session_manager,
    orchestrator_agent=orchestrator_agent,
)

# ------------------------------------------------------------------
# FastAPI Dependencies
# ------------------------------------------------------------------

def get_chat_service() -> ChatService:
    return chat_service


def get_session_manager() -> SessionManager:
    return session_manager


def get_http_client() -> httpx.AsyncClient:
    return http_client