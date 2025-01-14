from pathlib import Path
import os
from typing import Dict, Tuple, Union

# Базовые директории
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = BASE_DIR / "TgVideos"
DATABASE_DIR = BASE_DIR / "DataBase"

# Конфигурация медиа категорий
class MediaConfig:
    ANIMAL = MEDIA_DIR / "Animal"
    FUNNY = MEDIA_DIR / "Funny"
    
    @classmethod
    def create_dirs(cls) -> None:
        """Создает все необходимые директории, если они не существуют"""
        for path in [cls.ANIMAL, cls.FUNNY]:
            path.mkdir(parents=True, exist_ok=True)

# Настройки видео
VIDEO_SETTINGS = {
    "MAX_FILE_SIZE": 50 * 1024 * 1024,  # 50MB в байтах
    "ALLOWED_FORMATS": ["mp4"],
    "MIN_DURATION": 3,  # минимальная длительность видео в секундах
    "MAX_DURATION": 60  # максимальная длительность видео в секундах
}

# Конфигурация таймингов
TIMING = {
    "VIDEO_DOWNLOAD_LIMIT": 100,  # Максимальное количество видео для обработки на канал
    "VIDEO_SEND_DELAY": 1200,     # Задержка между отправкой видео
    "RETRY_DELAY": 60,            # Задержка перед повторной попыткой при ошибке (секунды)
    "UPDATE_INTERVAL": 90000      # Как часто проверять новые видео (секунды)
}

# Настройки базы данных
DB_CONFIG = {
    "path": DATABASE_DIR / "uita.db",
    "backup_path": DATABASE_DIR / "backups",
    "max_backup_count": 5,
    "backup_interval": 86400  # 24 часа в секундах
}

# Настройки логирования
LOGGING = {
    "max_file_size": 5 * 1024 * 1024,  # 5MB
    "backup_count": 10,
    "log_dir": BASE_DIR / "logs"
}

# Конфигурация каналов для загрузки
DOWNLOAD_CHANNEL: Dict[Tuple[int, ...], Path] = {
    (-1001080141747, -1001237893678, -1001701743745, -1001163478947, -1001951263817, -1001897631177, -1002079302764, -1002121784999, -1001692392564): MediaConfig.ANIMAL,
    (-1001154509246, -1001148195583, -1001520185750, -1001045540194, -1001123683328): MediaConfig.FUNNY
}

# Конфигурация моих каналов
MY_CHANNEL: Dict[Path, str] = {
    MediaConfig.ANIMAL: "-1002141467392",
    MediaConfig.FUNNY: "-1002124118502"
}

# Инициализация директорий
MediaConfig.create_dirs()

def validate_config() -> None:
    """Проверяет критические настройки конфигурации"""
    if not all(isinstance(chat_id, int) for chat_ids in DOWNLOAD_CHANNEL.keys() 
               for chat_id in chat_ids):
        raise ValueError("Все ID чатов должны быть целыми числами")
    
    if not all(isinstance(channel_id, str) for channel_id in MY_CHANNEL.values()):
        raise ValueError("Все ID целевых каналов должны быть строками")
    
    if not all(isinstance(path, Path) for path in MY_CHANNEL.keys()):
        raise ValueError("Все пути должны быть объектами Path")

# Запускаем валидацию при импорте
validate_config()

# Экспортируем необходимые переменные для обратной совместимости
VIDEO_DOWNLOAD_LIMIT = TIMING["VIDEO_DOWNLOAD_LIMIT"]
VIDEO_SEND_DELAY = TIMING["VIDEO_SEND_DELAY"]
