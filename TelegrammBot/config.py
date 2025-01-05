import os
from pathlib import Path
from typing import Dict, Tuple, Union

# Base directory for all media files
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
MEDIA_DIR = BASE_DIR / "TgVideos"

# Media categories configuration
class MediaConfig:
    ANIMAL = MEDIA_DIR / "Animal"
    FUNNY = MEDIA_DIR / "Funny"
    
    @classmethod
    def create_dirs(cls) -> None:
        """Create all necessary directories if they don't exist"""
        for path in [cls.ANIMAL, cls.FUNNY]:
            path.mkdir(parents=True, exist_ok=True)

# Video processing settings
VIDEO_SETTINGS = {
    "MAX_FILE_SIZE": 50 * 1024 * 1024,  # 50MB in bytes
    "ALLOWED_FORMATS": ["mp4"],
    "MIN_DURATION": 3,  # minimum video duration in seconds
    "MAX_DURATION": 60  # maximum video duration in seconds
}

# Bot timing configuration
TIMING = {
    "VIDEO_DOWNLOAD_LIMIT": 100,  # Maximum number of videos to process per channel
    "VIDEO_SEND_DELAY": 3000,     # Delay between sending videos (ms)
    "RETRY_DELAY": 60,            # Delay before retrying failed operations (seconds)
    "UPDATE_INTERVAL": 3600       # How often to check for new videos (seconds)
}

# Channel configurations
DOWNLOAD_CHANNEL: Dict[Tuple[int, ...], Path] = {
    (-1001951263817, -1001692392564, -1001237893678, -1001163478947, 
     -1001080141747, -1002079302764, -1001897631177): MediaConfig.ANIMAL,
    (-1001154509246, -1001886293489, -1001123683328, -1001045540194, 
     -1002087613865): MediaConfig.FUNNY
}

MY_CHANNEL: Dict[Path, str] = {
    MediaConfig.ANIMAL: "-1002141467392",
    MediaConfig.FUNNY: "-1002124118502"
}

# Database configuration
DB_CONFIG = {
    "path": BASE_DIR / "DataBase" / "uita.db",
    "backup_path": BASE_DIR / "DataBase" / "backups",
    "max_backup_count": 5
}

# Initialize directories
MediaConfig.create_dirs()

# Validation
def validate_config():
    """Validate critical configuration settings"""
    if not all(isinstance(delay, (int, float)) for delay in TIMING.values()):
        raise ValueError("All timing values must be numbers")
    
    if not all(isinstance(chat_id, int) for chat_ids in DOWNLOAD_CHANNEL.keys() 
               for chat_id in chat_ids):
        raise ValueError("All chat IDs must be integers")
    
    if not all(isinstance(channel_id, str) for channel_id in MY_CHANNEL.values()):
        raise ValueError("All target channel IDs must be strings")

# Run validation on import
validate_config()
