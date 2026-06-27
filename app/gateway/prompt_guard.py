import re

from app.exceptions.prompt_guard_exception import PromptGuardException


class PromptGuard:
    """
    Basic prompt injection detection.
    """

    BLOCKED_PATTERNS = [
        r"ignore\s+previous\s+instructions",
        r"ignore\s+all\s+instructions",
        r"system\s+prompt",
        r"developer\s+message",
        r"reveal\s+your\s+instructions",
        r"show\s+your\s+prompt",
        r"bypass\s+safety",
        r"jailbreak",
        r"act\s+as\s+root",
        r"pretend\s+to\s+be",
    ]

    @classmethod
    async def validate(cls, message: str) -> None:
        if not message:
            return

        normalized = message.lower()

        for pattern in cls.BLOCKED_PATTERNS:
            if re.search(pattern, normalized):
                raise PromptGuardException()