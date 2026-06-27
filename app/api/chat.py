from fastapi import APIRouter, Depends

from app.dependencies import get_chat_service
from app.models.requests.chat_request import ChatRequest
from app.models.requests.end_session_request import EndSessionRequest
from app.models.requests.start_session_request import (
    StartSessionRequest,
)
from app.models.responses.chat_response import ChatResponse
from app.models.responses.end_session_response import (
    EndSessionResponse,
)
from app.models.responses.start_session_response import (
    StartSessionResponse,
)
from app.services.interfaces.chat_service_interface import (
    IChatService,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/start",
    response_model=StartSessionResponse,
)
async def start_session(
    request: StartSessionRequest,
    chat_service: IChatService = Depends(get_chat_service),
) -> StartSessionResponse:

    return await chat_service.start_session(request)


@router.post(
    "",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
    chat_service: IChatService = Depends(get_chat_service),
) -> ChatResponse:

    return await chat_service.chat(request)


@router.post(
    "/end",
    response_model=EndSessionResponse,
)
async def end_session(
    request: EndSessionRequest,
    chat_service: IChatService = Depends(get_chat_service),
) -> EndSessionResponse:

    return await chat_service.end_session(request)