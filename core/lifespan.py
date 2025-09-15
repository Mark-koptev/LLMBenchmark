from contextlib import asynccontextmanager
from api.dependencies.services import get_redis_cache
from fastapi import FastAPI

from core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Сервис запущен")

    yield
    redis_cache = get_redis_cache()
    await redis_cache.close()
    logger.info("Сервис завершил работу")
