from fastapi import APIRouter

from .Benchmark import router as benchmark
from .Redis import router as redis

router = APIRouter(prefix="/api")

router.include_router(redis, tags=["Redis"])
router.include_router(benchmark, tags=["Benchmark"])
__all__ = ["router"]
