import asyncio
import os
import logging
from pathlib import Path

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError

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


SESSION_DIR = Path(__file__).parent / "sessions"
SESSION_FILE = SESSION_DIR / "tavrik.session"

os.makedirs(SESSION_DIR, exist_ok=True)

logger = logging.getLogger(__name__)

async def main():
    logger.info("Начало процесса авторизации")
    
    if SESSION_FILE.exists():
        logger.info("Найдена сохраненная сессия")
        with open(SESSION_FILE, 'r') as f:
            SESSION_STRING = f.read()
    else:
        logger.info("Сохраненная сессия не найдена, требуется новая авторизация")
        SESSION_STRING = None

    client = TelegramClient(StringSession(SESSION_STRING), TG_ID_API, TG_HASH_API)
    
    try:
        await client.start(phone=PHONE)
        
        if not await client.is_user_uthorized():
            logger.info("Пользователь не авторизован, запрашиваем код подтверждения")
            await client.send_code_request(PHONE)
            code = input('Введите код подтверждения: ')
            
            try:
                await client.sign_in(phone=PHONE, code=code)
            except SessionPasswordNeededError:
                logger.info("Требуется двухфакторная аутентификация")
                password = input('Введите пароль двухфакторной аутентификации: ')
                await client.sign_in(password=password)
        
        logger.info("Авторизация успешно завершена")
        # Сохраняем сессию в файл
        with open(SESSION_FILE, 'w') as f:
            f.write(client.session.save())
        
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
