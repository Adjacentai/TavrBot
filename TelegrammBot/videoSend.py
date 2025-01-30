import os
import asyncio
import logging

from dotenv import load_dotenv

from config import MY_CHANNEL, TIMING
from aiogram import Bot
from aiogram.types import FSInputFile

load_dotenv()
BOT_TOKEN = os.getenv('TG_TOKEN_BOT')

bot = Bot(token=BOT_TOKEN)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def send_my_videos(interval_smv: int, topic_smv: str):
    logger.info(f"Запуск сервиса отправки видео. Папка: {topic_smv}, Интервал: {interval_smv} сек")
    
    if not os.path.exists(topic_smv):
        logger.error(f"Директория {topic_smv} не существует")
        os.makedirs(topic_smv, exist_ok=True)
        logger.info(f"Создана директория {topic_smv}")
    
    while True:
        videos = os.listdir(topic_smv)
        
        if not videos:
            await asyncio.sleep(interval_smv)
            continue
        random.shuffle(videos)  # Перемешиваем список видео
        for video in videos:
            video_path = os.path.join(topic_smv, video)
            
            try:
                # Сначала отправляем видео
                await bot.send_video(MY_CHANNEL[topic_smv], FSInputFile(video_path))
                # Только после успешной отправки удаляем файл
                if os.path.exists(video_path):
                    os.remove(video_path)
                    logger.info(f"Видео {video} успешно отправлено и удалено")
                
                await asyncio.sleep(interval_smv)
            except Exception as e:
                logger.error(f"Ошибка при отправке видео {video}: {str(e)}")
                # При ошибке не удаляем файл, чтобы попробовать отправить снова
                await asyncio.sleep(TIMING["RETRY_DELAY"])
