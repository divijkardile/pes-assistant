from abc import ABC, abstractmethod

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


class IChatService(ABC):

    @abstractmethod
    async def start_session(
        self,
        request: StartSessionRequest,
    ) -> StartSessionResponse:
        """Start a new chat session."""
        ...

    @abstractmethod
    async def chat(
        self,
        request: ChatRequest,
    ) -> ChatResponse:
        """Process a chat request."""
        ...

    @abstractmethod
    async def end_session(
        self,
        request: EndSessionRequest,
    ) -> EndSessionResponse:
        """End an existing chat session."""
        ...