from email.policy import HTTP
from wsgiref import headers
from fastapi import HTTPException
import requests
from core.logger import logger

from repositories.Benchmark import BenchmarkRepository
from schemas.Benchmark import (
    ERole,
    SGenerateRequest,
    SGenerateResponse,
    SListModels,
    SMessage,
    SModel,
    SOpenRouterRequest,
    SOpenRouterResponse,
)
from config import settings


class BenchmarkService:
    def __init__(
        self,
        repository: BenchmarkRepository = BenchmarkRepository(),
    ) -> None:
        self.repository = repository
        self.api_key = settings.OPENAI_API_KEY

    async def get_headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def get_models(self):
        models = await self.repository.get_models()
        if not models:
            raise HTTPException(status_code=404, detail="Модели не найдены")

        models: list[SModel] = [SModel(**model) for model in models]
        return SListModels(models=models)

    async def generate(self, params: SGenerateRequest) -> SGenerateResponse:
        data: SOpenRouterRequest = SOpenRouterRequest(
            model=params.model,
            messages=[SMessage(role=ERole.USER, content=params.prompt)],
            max_tokens=params.max_tokens,
        )
        headers: dict[str, str] = await self.get_headers()
        open_router_response: SOpenRouterResponse = (
            await self.repository.get_chat_completions(
                data=data,
                headers=headers,
            )
        )
        return SGenerateResponse(
            text=open_router_response.first_message,
            token_used=open_router_response.usage,
        )

    # TODO доделать generate c stream=true
    # TODO доделать benchmark базовый и отверстать template для отображения сравнительной таблицы
