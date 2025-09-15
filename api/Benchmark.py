from fastapi import APIRouter, Depends, HTTPException
from schemas.Benchmark import SGenerateRequest, SGenerateResponse, SListModels

from api.dependencies.services import get_benchmark_service
from typing import Any

from services.Benchmark import BenchmarkService

router = APIRouter()


@router.get("/models", response_model=SListModels)
async def get_models(
    benchmark_service: BenchmarkService = Depends(get_benchmark_service),
) -> SListModels:
    models: SListModels = await benchmark_service.get_models()
    return models


@router.post("/generate")
async def generate(
    params: SGenerateRequest,
    benchmark_service: BenchmarkService = Depends(get_benchmark_service),
) -> SGenerateResponse:
    return await benchmark_service.generate(params)
