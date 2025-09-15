import logging
import os
from pathlib import Path

from config import settings


# Кастомный форматтер для логирования относительных путей
class RelativePathFormatter(logging.Formatter):
    def format(self, record):
        # Получаем абсолютный путь к файлу, где записан лог
        pathname = Path(record.pathname).resolve()
        # Преобразуем абсолютный путь к файлу в относительный относительно корня проекта
        record.relativepath = str(pathname.relative_to(settings.BASE_DIR))
        return super().format(record)


def setup_base_logger():
    # Настройка логирования с кастомным форматтером
    formatter = RelativePathFormatter(
        fmt="%(asctime)s [%(levelname)s] (%(relativepath)s:%(lineno)d) - %(message)s",  # Используем %(relativepath)s
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Настраиваем обработчики
    file_handler = logging.FileHandler(settings.LOG_PATH, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Настройка основного логгера
    logger = logging.getLogger(__name__)
    logger.setLevel(settings.LOG_LEVEL)
    logger.addHandler(file_handler)

    return logger


logger = setup_base_logger()
