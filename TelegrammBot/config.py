from dataclasses import dataclass
from pathlib import Path
import os
from typing import Dict, Tuple, Union

@dataclass
class Paths:
    BASE_DIR: Path = Path(os.path.dirname(os.path.abspath(__file__)))
    MEDIA_DIR: Path = BASE_DIR / "TgVideos"
    DATABASE_DIR: Path = BASE_DIR / "DataBase"

@dataclass
class VideoSettings:
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_FORMATS: tuple = ("mp4",)
    MIN_DURATION: int = 3
    MAX_DURATION: int = 60

@dataclass
class TimingSettings:
    VIDEO_DOWNLOAD_LIMIT: int = 100
    VIDEO_SEND_DELAY: int = 1200
    RETRY_DELAY: int = 60
    UPDATE_INTERVAL: int = 90000

paths = Paths()
video_settings = VideoSettings()
timing = TimingSettings()

# Конфигурация медиа категорий
class MediaConfig:
    ANIMAL = paths.MEDIA_DIR / "Animal"
    FUNNY = paths.MEDIA_DIR / "Funny"
    
    @classmethod
    def create_dirs(cls) -> None:
        """Создает все необходимые директории, если они не существуют"""
        for path in [cls.ANIMAL, cls.FUNNY]:
            path.mkdir(parents=True, exist_ok=True)

# Настройки видео
VIDEO_SETTINGS = {
    "MAX_FILE_SIZE": video_settings.MAX_FILE_SIZE,  # 50MB в байтах
    "ALLOWED_FORMATS": video_settings.ALLOWED_FORMATS,
    "MIN_DURATION": video_settings.MIN_DURATION,  # минимальная длительность видео в секундах
    "MAX_DURATION": video_settings.MAX_DURATION  # максимальная длительность видео в секундах
}

# Конфигурация таймингов
TIMING = {
    "VIDEO_DOWNLOAD_LIMIT": timing.VIDEO_DOWNLOAD_LIMIT,  # Максимальное количество видео для обработки на канал
    "VIDEO_SEND_DELAY": timing.VIDEO_SEND_DELAY,     # Задержка между отправкой видео
    "RETRY_DELAY": timing.RETRY_DELAY,            # Задержка перед повторной попыткой при ошибке (секунды)
    "UPDATE_INTERVAL": timing.UPDATE_INTERVAL      # Как часто проверять новые видео (секунды)
}

# Настройки базы данных
DB_CONFIG = {
    "path": paths.DATABASE_DIR / "uita.db",
    "backup_path": paths.DATABASE_DIR / "backups",
    "max_backup_count": 5,
    "backup_interval": 86400  # 24 часа в секундах
}

# Настройки логирования
LOGGING = {
    "max_file_size": 5 * 1024 * 1024,  # 5MB
    "backup_count": 10,
    "log_dir": paths.BASE_DIR / "logs"
}

# Конфигурация каналов для загрузки
DOWNLOAD_CHANNEL: Dict[Tuple[int, ...], Path] = {
    (-1001237893678, -1001452243311, -1001398033365, -1001235005907, -1001500454306, -1001433508046, -1001555710621, -1001689907832, -1001697846192, -1001460470667): MediaConfig.ANIMAL
    #(-1001154509246, -1001148195583, -1001520185750, -1001045540194, -1001123683328): MediaConfig.FUNNY
}

# Конфигурация моих каналов
MY_CHANNEL: Dict[Path, str] = {
    MediaConfig.ANIMAL: "-1002141467392"
    # MediaConfig.FUNNY: "-1002124118502"
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
