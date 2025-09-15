import logging
import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pydantic import Field
import logging


class Settings(BaseSettings):

    OPENAI_API_KEY: str
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_LEVEL: int = logging.INFO
    REDIS_HOST: str = Field(default=...)
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def LOG_DIR(self) -> str:
        return os.path.join(self.BASE_DIR, "log")

    @property
    def LOG_PATH(self) -> str:
        return os.path.join(self.LOG_DIR, "service_utils.log")

    @property
    def TMP_DIR(self) -> str:
        return os.path.join(self.BASE_DIR, "tmp")


def create_directories(settings: Settings):
    """Создает необходимые директории"""
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    os.makedirs(settings.TMP_DIR, exist_ok=True)


# @lru_cache
def get_settings() -> Settings:
    settings = Settings()
    create_directories(settings)
    return settings


settings = get_settings()
