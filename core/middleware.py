from fastapi import Request
from core.logger import logger


async def logging_middleware(request: Request, call_next):
    """
    Middleware для логирования каждого входящего запроса
    """

    user_login = request.headers.get("x-user-login", "Анонимный пользователь")

    logger.info(
        f"Request: Пользователь '{user_login}' -> {request.method} {request.url.path} с IP {request.client.host}"
    )

    response = await call_next(request)

    logger.info(
        f"Response: Для '{user_login}' -> {request.method} {request.url.path} | Статус: {response.status_code}"
    )

    return response
