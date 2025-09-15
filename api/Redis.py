from fastapi import APIRouter, Depends, HTTPException
from schemas.Benchmark import SListModels

from api.dependencies.services import get_benchmark_service, get_redis_cache
from typing import Any

from services.Benchmark import BenchmarkService
from services.Redis import RedisCacheService

router = APIRouter()


@router.get("/clear-cache")
async def clear_cache(redis_cache: RedisCacheService = Depends(get_redis_cache)):
    await redis_cache.flush()
    return {"message": "Cache cleared successfully"}
