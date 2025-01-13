from pathlib import Path
from typing import Dict, Tuple, Union
from constants import MEDIA_DIR

# Конфигурация медиа категорий
class MediaConfig:
    ANIMAL = MEDIA_DIR / "Animal"
    FUNNY = MEDIA_DIR / "Funny"
    
    @classmethod
    def create_dirs(cls) -> None:
        """Создает все необходимые директории, если они не существуют"""
        for path in [cls.ANIMAL, cls.FUNNY]:
            path.mkdir(parents=True, exist_ok=True)

# Конфигурация каналов для загрузки
DOWNLOAD_CHANNEL: Dict[Tuple[int, ...], Path] = {
    (-1001951263817, -1001692392564, -1001237893678, -1001163478947, 
     -1001080141747, -1002079302764, -1001897631177): MediaConfig.ANIMAL,
    (-1001154509246, -1001886293489, -1001123683328, -1001045540194, 
     -1002087613865): MediaConfig.FUNNY
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
