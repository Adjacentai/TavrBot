import os
import asyncio
import logging

from dotenv import load_dotenv

from config import MY_CHANNEL
from aiogram import Bot
from aiogram.types import FSInputFile

load_dotenv()
BOT_TOKEN = os.getenv('TG_TOKEN_BOT')

bot = Bot(token=BOT_TOKEN)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def send_my_videos(interval_smv: int, topic_smv: str):
    while True:
        videos = os.listdir(topic_smv)
        if not videos:
            await asyncio.sleep(interval_smv)
            continue

        for video in videos:
            video_path = os.path.join(topic_smv, video)
            try:
                await bot.send_video(MY_CHANNEL[topic_smv], FSInputFile(video_path))
            except Exception as e:
                logger.info(f"failed to send video {video}: {e}")
                continue
            else:
                os.remove(video_path)
                logger.info(f"VIDEO {video} SENT TO {MY_CHANNEL[topic_smv]} SUCCESSFULLY.")

            await asyncio.sleep(interval_smv)
