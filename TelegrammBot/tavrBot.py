import asyncio
import os
import logging
from pathlib import Path

from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError, SessionExpiredError

from videoDownload import download_tg_videos
from videoSend import send_my_videos
from DataBase.dbConfig import init_db
from config import (
    MediaConfig,
    TIMING
)
from entity import get_entities
from utils.logger import setup_logger

load_dotenv()

TG_ID_API = os.getenv('TG_ID_API')
TG_HASH_API = os.getenv('TG_HASH_API')
PHONE = os.getenv('PHONE')

SESSION_DIR = Path(__file__).parent / "sessions"
SESSION_FILE = SESSION_DIR / "tavrik.session"

os.makedirs(SESSION_DIR, exist_ok=True)

logger = setup_logger('tavrBot', Path(__file__).parent / 'logs')

async def main():
    logger.info("Начало процесса авторизации")
    
    SESSION_STRING = None
    if SESSION_FILE.exists():
        logger.info("Найдена сохраненная сессия")
        try:
            with open(SESSION_FILE, 'rb') as f:
                session_data = f.read()
                SESSION_STRING = session_data.decode('utf-8', errors='replace')
                logger.info("Сессия успешно загружена")
        except Exception as e:
            logger.error(f"Ошибка при чтении файла сессии: {e}")
            logger.info("Создаем новую сессию")

    client = TelegramClient(StringSession(SESSION_STRING), TG_ID_API, TG_HASH_API)
    
    try:
        await client.start(phone=PHONE)
        
        if not await client.is_user_authorized():
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
        with open(SESSION_FILE, 'wb') as f:
            session_data = client.session.save()
            f.write(session_data.encode('utf-8'))
        
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
