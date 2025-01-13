from pathlib import Path
import os

# Базовые директории
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = BASE_DIR / "TgVideos"
DATABASE_DIR = BASE_DIR / "DataBase"

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
    "VIDEO_SEND_DELAY": 3000,     # Задержка между отправкой видео (мс)
    "RETRY_DELAY": 60,            # Задержка перед повторной попыткой при ошибке (секунды)
    "UPDATE_INTERVAL": 3600       # Как часто проверять новые видео (секунды)
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