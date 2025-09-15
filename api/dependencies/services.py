from repositories.Benchmark import BenchmarkRepository
from services.Benchmark import BenchmarkService
from services.Redis import RedisCacheService, redis_cache


def get_redis_cache() -> RedisCacheService:
    return redis_cache


def get_benchmark_service() -> BenchmarkService:
    repository = BenchmarkRepository()

    return BenchmarkService(repository=repository)
