import asyncio
import os

from dotenv import load_dotenv
from telethon import TelegramClient

from videoDownload import download_tg_videos
from videoSend import send_my_videos
from config import ANIMAL, FUNNY
from DataBase.dbConfig import init_db

load_dotenv()

TgUserBot_ID = os.getenv('TgUserBot_ID_SLVK')
TgUserBot_HASH = os.getenv('TgUserBot_HASH_SLVK')


async def main():
    async with  TelegramClient('SOSESSION', TgUserBot_ID, TgUserBot_HASH) as client:
        while True:
            await asyncio.gather(
                download_tg_videos(client, 100),
                send_my_videos(3000, ANIMAL),
                send_my_videos(3000, FUNNY)
            )


if __name__ == '__main__':
    asyncio.run(init_db())
    asyncio.run(main())
