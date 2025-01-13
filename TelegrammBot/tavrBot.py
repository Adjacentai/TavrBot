import asyncio
import os

from dotenv import load_dotenv
from telethon import TelegramClient

from videoDownload import download_tg_videos
from videoSend import send_my_videos
from config import ANIMAL, FUNNY, VIDEO_DOWNLOAD_LIMIT, VIDEO_SEND_DELAY
from DataBase.dbConfig import init_db

load_dotenv()

TG_ID_API = os.getenv('TG_ID_API')
TG_HASH_API = os.getenv('TG_HASH_API')
PHONE = os.getenv('PHONE')

async def main():
    client = TelegramClient('chatbot', TG_ID_API, TG_HASH_API)
    await client.start(phone=PHONE)
    
    if not await client.is_user_authorized():
        await client.send_code_request(PHONE)
        code = input('Введите код подтверждения: ')
        await client.sign_in(PHONE, code)
    
    while True:
        await asyncio.gather(
            download_tg_videos(client, VIDEO_DOWNLOAD_LIMIT),
            send_my_videos(VIDEO_SEND_DELAY, ANIMAL),
            send_my_videos(VIDEO_SEND_DELAY, FUNNY)
            # entity_adding(client) - look at videoDownload.py
        )



if __name__ == '__main__':
    asyncio.run(init_db())
    asyncio.run(main())
