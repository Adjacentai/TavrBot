import logging
import logging.handlers
import os
from pathlib import Path

def setup_logger(name: str, log_dir: Path, max_size: int = 5*1024*1024, backup_count: int = 10) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    os.makedirs(log_dir, exist_ok=True)
    
    # Файловый обработчик с ротацией
    file_handler = logging.handlers.RotatingFileHandler(
        log_dir / f"{name}.log",
        maxBytes=max_size,
        backupCount=backup_count,
        encoding='utf-8'
    )
    
    # Консольный обработчик
    console_handler = logging.StreamHandler()
    
    # Форматирование
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger 