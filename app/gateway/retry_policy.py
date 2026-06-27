import asyncio
import logging
from typing import Any, Awaitable, Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


class RetryPolicy:
    """
    Generic retry policy for transient failures.
    """

    def __init__(
        self,
        *,
        max_retries: int,
        initial_delay: float,
        backoff_multiplier: float,
        retry_exceptions: tuple[type[Exception], ...] = (Exception,),
    ) -> None:
        self._max_retries = max_retries
        self._initial_delay = initial_delay
        self._backoff_multiplier = backoff_multiplier
        self._retry_exceptions = retry_exceptions

    async def execute(
        self,
        operation: Callable[..., Awaitable[T]],
        *args: Any,
        **kwargs: Any,
    ) -> T:
        delay = self._initial_delay
        last_exception: Exception | None = None

        for attempt in range(1, self._max_retries + 2):
            try:
                return await operation(*args, **kwargs)

            except self._retry_exceptions as ex:
                last_exception = ex

                if attempt > self._max_retries:
                    logger.exception(
                        "Operation failed after %s attempts.",
                        attempt,
                    )
                    break

                logger.warning(
                    "Retry attempt %s/%s after error: %s",
                    attempt,
                    self._max_retries,
                    ex,
                )

                await asyncio.sleep(delay)
                delay *= self._backoff_multiplier

        if last_exception:
            raise last_exception

        raise RuntimeError("RetryPolicy reached an unexpected state.")