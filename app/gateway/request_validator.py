from app.exceptions.validation_exception import ValidationException
from app.models.requests.chat_request import ChatRequest


class RequestValidator:
    """
    Validates incoming AI chat requests.
    """

    @staticmethod
    async def validate(request: ChatRequest) -> None:
        if request is None:
            raise ValidationException("Request cannot be null.")

        if not request.session_id:
            raise ValidationException("Session ID is required.")

        if not request.message:
            raise ValidationException("Message is required.")

        if not request.message.strip():
            raise ValidationException("Message cannot be empty.")