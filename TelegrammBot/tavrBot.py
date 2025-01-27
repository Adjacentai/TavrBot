import asyncio
import os
import logging

from dotenv import load_dotenv
from telethon import TelegramClient

from videoDownload import download_tg_videos
from videoSend import send_my_videos
from DataBase.dbConfig import init_db
from config import (
    MediaConfig,
    TIMING,
)
from entity import get_entities

load_dotenv()

TG_ID_API = os.getenv('TG_ID_API')
TG_HASH_API = os.getenv('TG_HASH_API')
PHONE = os.getenv('PHONE')

logger = logging.getLogger(__name__)

async def main():
    client = TelegramClient('Plication', TG_ID_API, TG_HASH_API)
    
    try:
        await client.start(phone=PHONE)
        
        if not await client.is_user_authorized():
            await client.send_code_request(PHONE)
            code = input('Введите код подтверждения: ')
            await client.sign_in(PHONE, code)
        
        await get_entities(client)
        
        while True:
            await asyncio.gather(
                download_tg_videos(client, TIMING["VIDEO_DOWNLOAD_LIMIT"]),
                send_my_videos(TIMING["VIDEO_SEND_DELAY"], MediaConfig.ANIMAL)
            )
    except KeyboardInterrupt:
        logger.info("Получен сигнал завершения программы")
    except Exception as e:
        logger.error(f"Произошла ошибка: {e}")

if __name__ == '__main__':
    asyncio.run(init_db())
    asyncio.run(main())