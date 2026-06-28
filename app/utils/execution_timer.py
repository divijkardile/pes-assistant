import asyncio
import logging
import time
from functools import wraps
from typing import Any, Callable, Coroutine

from app.config.settings import get_settings


def execution_timer(func: Callable) -> Callable:
    """
    Decorator to track function execution time.
    
    Logs execution duration for both sync and async functions.
    
    Usage:
        @execution_timer
        async def my_function():
            pass
            
        @execution_timer
        def sync_function():
            pass
    """

    @wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        logger = logging.getLogger(func.__module__)
        start_time = time.time()
        func_name = func.__name__

        logger.info(
            f"[TIMER] Starting execution: {func_name}",
        )

        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time

            logger.info(
                f"[TIMER] Completed: {func_name} "
                f"(Duration: {execution_time:.4f}s)",
            )

            return result

        except Exception as e:
            execution_time = time.time() - start_time

            logger.error(
                f"[TIMER] Failed: {func_name} "
                f"(Duration: {execution_time:.4f}s) - Error: {str(e)}",
            )
            raise

    @wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        logger = logging.getLogger(func.__module__)
        start_time = time.time()
        func_name = func.__name__

        logger.info(
            f"[TIMER] Starting execution: {func_name}",
        )

        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time

            logger.info(
                f"[TIMER] Completed: {func_name} "
                f"(Duration: {execution_time:.4f}s)",
            )

            return result

        except Exception as e:
            execution_time = time.time() - start_time

            logger.error(
                f"[TIMER] Failed: {func_name} "
                f"(Duration: {execution_time:.4f}s) - Error: {str(e)}",
            )
            raise

    # Check if function is async
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
