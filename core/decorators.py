import asyncio
import time
from functools import wraps
from typing import Callable, Any
from core.logger import logger


def measure_time(func: Callable) -> Callable:
    """
    Декоратор для измерения времени выполнения функции.
    Работает с синхронными и асинхронными функциями.
    """

    @wraps(func)
    async def async_wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        try:
            result = await func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start_time
            logger.info(f"Функция {func.__name__} выполнилась за {elapsed:.6f} секунд")
        return result

    @wraps(func)
    def sync_wrapper(*args, **kwargs) -> Any:
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        finally:
            elapsed = time.perf_counter() - start_time
            logger.info(f"Функция {func.__name__} выполнилась за {elapsed:.6f} секунд")
        return result

    return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper


def exception_handler(func: Callable) -> Callable:
    """
    Декоратор для обработки исключений.
    Работает с синхронными и асинхронными функциями.
    """

    if asyncio.iscoroutinefunction(func):

        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any):
            try:
                result = await func(*args, **kwargs)
            except Exception as e:
                print(f"В функции {func.__name__} произошло исключение: {e}")
                result = None
            return result

        return async_wrapper
    else:

        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any):
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                print(f"В функции {func.__name__} произошло исключение: {e}")
                result = None
            return result

        return sync_wrapper
