from functools import wraps
import hashlib
import json
from typing import Any, Optional, Dict
from redis.asyncio import Redis
from redis.exceptions import RedisError

from config import settings


class RedisCacheService:
    """
    Асинхронный клиент для работы с Redis-кешем
    """

    def __init__(
        self,
        redis_client: Redis,
        default_ttl: int = 3600,
        serializer: callable = json.dumps,
        deserializer: callable = json.loads,
    ):
        """
        Инициализация кеш-клиента

        :param redis_client: Async Redis client
        :param default_ttl: Время жизни записей по умолчанию (в секундах)
        :param serializer: Функция для сериализации данных
        :param deserializer: Функция для десериализации данных
        """
        self.redis = redis_client
        self.default_ttl = default_ttl
        self.serializer = serializer
        self.deserializer = deserializer

    async def pong(self):
        return await self.redis.ping()

    async def get(self, key: str, deserializer=None) -> Optional[Any]:
        """
        Получение значения по ключу
        """
        try:
            deserializer = deserializer or self.deserializer
            data = await self.redis.get(key)
            return deserializer(data) if data else None
        except RedisError as e:
            raise CacheError("Redis get operation failed") from e

    async def set(
        self, key: str, value: Any, ttl: Optional[int] = None, serializer=None
    ) -> bool:
        """
        Установка значения с TTL
        """

        try:
            serializer = serializer or self.serializer
            serialized = serializer(value, default=str)
            expire = ttl if ttl is not None else self.default_ttl
            return await self.redis.set(name=key, value=serialized, ex=expire)
        except RedisError as e:
            raise CacheError("Redis set operation failed") from e

    async def delete(self, *keys: str) -> int:
        """
        Удаление одного или нескольких ключей
        """
        try:
            return await self.redis.delete(*keys)
        except RedisError as e:
            raise CacheError("Redis delete operation failed") from e

    async def exists(self, key: str) -> bool:
        """
        Проверка существования ключа
        """
        try:
            return await self.redis.exists(key) == 1
        except RedisError as e:
            raise CacheError("Redis exists operation failed") from e

    async def expire(self, key: str, ttl: int) -> bool:
        """
        Установка времени жизни ключа в секундах
        """
        try:
            return await self.redis.expire(key, ttl)
        except RedisError as e:
            raise CacheError("Redis expire operation failed") from e

    async def ttl(self, key: str) -> int:
        """
        Получение оставшегося времени жизни ключа
        """
        try:
            return await self.redis.ttl(key)
        except RedisError as e:
            raise CacheError("Redis ttl operation failed") from e

    async def hget(self, key: str, field: str) -> Optional[Any]:
        """
        Получение значения из хэша
        """
        try:
            data = await self.redis.hget(key, field)
            return self.deserializer(data) if data else None
        except RedisError as e:
            raise CacheError("Redis hget operation failed") from e

    async def hset(
        self, key: str, field: str, value: Any, ttl: Optional[int] = None
    ) -> None:
        """
        Установка значения в хэш
        """
        try:
            serialized = self.serializer(value)
            await self.redis.hset(key, field, serialized)
            if ttl is not None:
                await self.redis.expire(key, ttl)
        except RedisError as e:
            raise CacheError("Redis hset operation failed") from e

    async def hgetall(self, key: str) -> Dict[str, Any]:
        """
        Получение всего хэша
        """
        try:
            data = await self.redis.hgetall(key)
            return {k: self.deserializer(v) for k, v in data.items()}
        except RedisError as e:
            raise CacheError("Redis hgetall operation failed") from e

    async def flush(self) -> bool:
        """
        Очистка всей базы данных
        """
        try:
            return await self.redis.flushdb()
        except RedisError as e:
            raise CacheError("Redis flush operation failed") from e

    async def close(self) -> None:
        """
        Закрытие соединения
        """
        await self.redis.close()


class CacheError(Exception):
    """Базовое исключение для ошибок кеширования"""

    pass


def cache_result(
    prefix_key: str = "",
    kwargs_names_to_keys: list[str] = ["default"],
    ttl: int = 3600,
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = prefix_key + func.__name__
            for key_name in kwargs_names_to_keys:
                key += str(kwargs.get(key_name, ""))

            key_data = hashlib.md5(key.encode()).hexdigest()
            if await redis_cache.exists(key_data):
                return await redis_cache.get(key_data)
            fresh_value = await func(*args, **kwargs)

            await redis_cache.set(key_data, fresh_value, ttl)
            return fresh_value

        return wrapper

    return decorator


redis_client = Redis.from_url(f"redis://{settings.REDIS_HOST}:6379")

redis_cache = RedisCacheService(redis_client)

__all__ = ["redis_cache", "cache_result"]
