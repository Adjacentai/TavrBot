import logging
import logging.handlers
import os
from pathlib import Path

# Создаем директорию для логов
log_dir = Path(__file__).parent / "logs"
log_dir.mkdir(exist_ok=True)

def setup_logger(name: str) -> logging.Logger:
    """
    Настраивает и возвращает logger с ротацией файлов
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Форматтер для логов
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Хендлер для файла с ротацией (10 файлов по 5MB каждый)
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / f"{name}.log",
        maxBytes=5*1024*1024,  # 5MB
        backupCount=10,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Хендлер для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Добавляем хендлеры к логгеру
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger 