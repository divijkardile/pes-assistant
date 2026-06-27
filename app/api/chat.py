from fastapi import APIRouter, Depends, HTTPException, status

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
from app.services.chat_service import ChatService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "/start",
    response_model=StartSessionResponse,
    status_code=status.HTTP_200_OK,
)
async def start_session(
    request: StartSessionRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> StartSessionResponse:
    try:
        return await chat_service.start_session(request)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex),
        ) from ex


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    try:
        return await chat_service.chat(request)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex),
        ) from ex


@router.post(
    "/end",
    response_model=EndSessionResponse,
    status_code=status.HTTP_200_OK,
)
async def end_session(
    request: EndSessionRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> EndSessionResponse:
    try:
        return await chat_service.end_session(request)
    except Exception as ex:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(ex),
        ) from ex