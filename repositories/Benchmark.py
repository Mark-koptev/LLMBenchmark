import json
import time
from typing import Optional, Dict
from fastapi import HTTPException
import requests
from schemas.Benchmark import (
    SListModels,
    SModel,
    SOpenRouterRequest,
    SOpenRouterResponse,
)
from services.Redis import cache_result


class BenchmarkRepository:

    @cache_result(prefix_key="models", ttl=3600)
    async def get_models(
        self,
    ) -> SListModels:
        models = requests.get("https://openrouter.ai/api/v1/models")
        if models.status_code != 200:
            raise HTTPException(
                status_code=models.status_code,
                detail=models.json()["error"]["message"],
            )
        return models.json()["data"]

    async def get_chat_completions(
        self,
        headers: Dict[str, str],
        data: SOpenRouterRequest,
    ) -> str:
        start_time = time.time()
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=data.model_dump_json(exclude_none=True),
        )
        # TODO доделать правильный подсчет latency
        end_time = time.time()
        latency_seconds = end_time - start_time
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()["error"]["message"],
            )
        open_router_response = SOpenRouterResponse(**response.json())
        return open_router_response
