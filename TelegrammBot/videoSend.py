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
    logger.info(f"Запуск сервиса отправки видео. Папка: {topic_smv}, Интервал: {interval_smv} сек")
    
    if not os.path.exists(topic_smv):
        logger.error(f"Директория {topic_smv} не существует")
        os.makedirs(topic_smv, exist_ok=True)
        logger.info(f"Создана директория {topic_smv}")
    
    while True:
        videos = os.listdir(topic_smv)
        videos_count = len(videos)
        
        if not videos:
            logger.debug(f"Нет видео в директории {topic_smv}")
            await asyncio.sleep(interval_smv)
            continue
        
        logger.info(f"Найдено {videos_count} видео в директории {topic_smv}")

        for video in videos:
            video_path = os.path.join(topic_smv, video)
            file_size = os.path.getsize(video_path)
            
            logger.info(f"Отправка видео {video} ({file_size} байт) в канал {MY_CHANNEL[topic_smv]}")
            
            try:
                await bot.send_video(MY_CHANNEL[topic_smv], FSInputFile(video_path))
            except Exception as e:
                logger.error(f"Ошибка при отправке видео {video}: {str(e)}\n"
                           f"Путь: {video_path}\n"
                           f"Размер: {file_size} байт\n"
                           f"Канал: {MY_CHANNEL[topic_smv]}")
                if os.path.exists(video_path):
                    os.remove(video_path)
                    logger.info(f"Файл {video} удален после ошибки отправки")
                continue
            else:
                os.remove(video_path)
                logger.info(f"Видео {video} успешно отправлено в канал {MY_CHANNEL[topic_smv]}")

            await asyncio.sleep(interval_smv)
