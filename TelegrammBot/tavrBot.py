import asyncio
import os
import logging
from pathlib import Path

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

from videoDownload import download_tg_videos
from videoSend import send_my_videos
from DataBase.dbConfig import init_db
from config import (
    MediaConfig,
    TIMING
)
from entity import get_entities

load_dotenv()

TG_ID_API = os.getenv('TG_ID_API')
TG_HASH_API = os.getenv('TG_HASH_API')
PHONE = os.getenv('PHONE')


SESSION_STRING = os.getenv('SESSION_STRING')

SESSION_DIR = Path(__file__).parent / "sessions"
SESSION_FILE = "/TelegrammBot/sessions/tavrik.session"

os.makedirs(SESSION_DIR, exist_ok=True)

logger = logging.getLogger(__name__)

async def main():
    client = TelegramClient(SESSION_FILE, TG_ID_API, TG_HASH_API)
    
    try:
        await client.start(phone=PHONE)
        
        if not await client.is_user_authorized():
            await client.send_code_request(PHONE)
            code = input('Введите код подтверждения: ')
            password = input('Введите пароль двухфакторной аутентификации: ')
            await client.sign_in(phone=PHONE, code=code, password=password)
        
        await get_entities(client)
        
        while True:
            try:
                await asyncio.gather(
                    download_tg_videos(client, TIMING["VIDEO_DOWNLOAD_LIMIT"]),
                    send_my_videos(TIMING["VIDEO_SEND_DELAY"], MediaConfig.ANIMAL)
                )
            except Exception as e:
                logger.error(f"Ошибка в основном цикле: {e}")
                await asyncio.sleep(TIMING["RETRY_DELAY"])
    except KeyboardInterrupt:
        logger.info("Получен сигнал завершения программы")
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")
    finally:
        await client.disconnect()

if __name__ == '__main__':
    asyncio.run(init_db())
    asyncio.run(main())
