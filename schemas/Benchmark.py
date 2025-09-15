from datetime import datetime
from enum import Enum
from os import error
from tkinter import E
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional


class ArchitectureModel(BaseModel):
    modality: str = Field(
        description="Модальность модели (формат входных/выходных данных)",
        examples=["text->text"],
    )
    input_modalities: List[str] = Field(
        description="Поддерживаемые входные модальности", examples=[["text"]]
    )
    output_modalities: List[str] = Field(
        description="Поддерживаемые выходные модальности", examples=[["text"]]
    )
    tokenizer: str = Field(
        description="Токенизатор, используемый моделью", examples=["Qwen3"]
    )
    instruct_type: Optional[str] = Field(
        description="Тип инструкций, которые понимает модель", examples=[None]
    )


class TopProviderModel(BaseModel):
    context_length: Optional[int] = Field(
        description="Длина контекста у топ-провайдера", examples=[262144]
    )
    max_completion_tokens: Optional[int] = Field(
        description="Максимальное количество токенов для завершения", examples=[None]
    )
    is_moderated: Optional[bool] = Field(
        description="Флаг модерации контента", examples=[False]
    )


class SModel(BaseModel):
    id: str = Field(
        description="Уникальный идентификатор модели",
        examples=["qwen/qwen3-next-80b-a3b-thinking"],
    )
    canonical_slug: Optional[str] = Field(
        description="Каноническое название модели для API",
        examples=["qwen/qwen3-next-80b-a3b-thinking-2509"],
    )
    hugging_face_id: Optional[str] = Field(
        description="Идентификатор модели на Hugging Face",
        examples=["Qwen/Qwen3-Next-80B-A3B-Thinking"],
    )
    name: str = Field(
        description="Человекочитаемое название модели",
        examples=["Qwen: Qwen3 Next 80B A3B Thinking"],
    )
    created: int = Field(
        description="Время создания модели в формате Unix timestamp",
        examples=[1757612284],
    )
    description: str = Field(
        description="Подробное описание модели и её возможностей",
        examples=["Qwen3-Next-80B-A3B-Thinking is a reasoning-first chat model..."],
    )
    context_length: int = Field(
        description="Максимальная длина контекста в токенах", examples=[262144]
    )
    architecture: ArchitectureModel = Field(
        description="Архитектурные характеристики модели"
    )
    pricing: dict = Field(description="Цены на модель", examples=[None])
    top_provider: TopProviderModel = Field(
        description="Информация о основном провайдере модели"
    )
    per_request_limits: Optional[Any] = Field(
        description="Ограничения на запросы", examples=[None]
    )
    supported_parameters: List[str] = Field(
        description="Список поддерживаемых параметров API",
        examples=[["frequency_penalty", "include_reasoning", "logit_bias"]],
    )


class SListModels(BaseModel):
    models: list[SModel] = Field(
        description="Список моделей",
    )


class SGenerateRequest(BaseModel):
    prompt: str = Field(
        default=...,
        description="Текст запроса",
        examples=["Hello, how are you?"],
    )
    model: str = Field(
        default=...,
        description="Идентификатор модели",
        examples=["qwen/qwen3-next-80b-a3b-thinking"],
    )
    max_tokens: int = Field(
        default=512,
        description="Максимальное количество генерируемых токенов",
        examples=[512],
    )


class ERole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    DEVELOPER = "developer"
    TOOL = "tool"
    DEFAULT = "user"


class SMessage(BaseModel):
    role: ERole
    content: str = Field(
        default=...,
        description="Текст сообщения",
        examples=["Hello, how are you?"],
    )
    refusal: Optional[str] = Field(
        default="",
        description="Текст отказа модели отвечать (если применимо)",
        examples=["", "I cannot answer that question"],
    )


class SOpenRouterRequest(BaseModel):
    model: str = Field(
        default=...,
        description="Идентификатор модели",
        examples=["qwen/qwen3-next-80b-a3b-thinking"],
    )
    messages: List[SMessage] = Field(
        default=...,
        description="Список сообщений",
    )
    max_tokens: int = Field(
        default=512,
        description="Максимальное количество генерируемых токенов",
        examples=[512],
    )


class Choice(BaseModel):
    message: SMessage = Field(description="Сообщение от ассистента")
    logprobs: Optional[dict] = None
    finish_reason: str = Field(
        description="Причина завершения генерации",
        examples=["stop", "length", "content_filter", "tool_calls"],
    )
    index: int = Field(description="Индекс выбора в списке choices", examples=[0])


class SUsage(BaseModel):
    prompt_tokens: int = Field(
        description="Количество токенов в промпте", examples=[14]
    )
    completion_tokens: int = Field(
        description="Количество токенов в ответе", examples=[163]
    )
    total_tokens: int = Field(description="Общее количество токенов", examples=[177])


class SOpenRouterResponse(BaseModel):
    success: bool = True
    error: Optional[str] = None
    id: str = Field(
        description="Уникальный идентификатор запроса", examples=["gen-12345"]
    )
    choices: List[Choice] = Field(description="Список вариантов ответа")
    provider: str = Field(
        description="Провайдер модели", examples=["OpenAI", "Anthropic", "Cohere"]
    )
    model: str = Field(
        description="Идентификатор модели",
        examples=["openai/gpt-3.5-turbo", "anthropic/claude-3-opus"],
    )
    object: str = Field(description="Тип объекта ответа", examples=["chat.completion"])
    created: int = Field(
        description="Время создания ответа в Unix timestamp", examples=[1735317796]
    )
    system_fingerprint: Optional[Dict[str, Any]] = Field(
        default_factory=dict, description="Отпечаток системы для воспроизводимости"
    )
    usage: SUsage = Field(description="Информация об использовании токенов")

    # Дополнительные computed properties
    @property
    def created_datetime(self) -> datetime:
        """Возвращает datetime объект времени создания"""
        return datetime.fromtimestamp(self.created)

    @property
    def first_choice(self) -> Choice:
        """Возвращает первый choice"""
        return self.choices[0]

    @property
    def first_message(self) -> str:
        """Возвращает текст первого сообщения"""
        return self.choices[0].message.content

    @property
    def total_cost(
        self, prompt_price: float = 0.0000005, completion_price: float = 0.0000015
    ) -> float:
        """Рассчитывает примерную стоимость запроса"""
        return (
            self.usage.prompt_tokens * prompt_price
            + self.usage.completion_tokens * completion_price
        )


class SLatency(BaseModel):
    http_code: int
    response_size: int
    connect_time: float
    time_total: float
    error: str


class SGenerateResponse(BaseModel):
    text: str
    token_used: SUsage | None = None
