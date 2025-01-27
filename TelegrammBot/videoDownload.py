import os
import asyncio
import logging
from DataBase.dbConfig import video_db_check, video_db_save

from telethon.tl.types import MessageMediaDocument
from config import DOWNLOAD_CHANNEL, TIMING, VIDEO_SETTINGS


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def download_tg_videos(client, limit: int):
    try:
        for chat_ids, folder in DOWNLOAD_CHANNEL.items():
            os.makedirs(folder, exist_ok=True)

            for chat_id in chat_ids:
                try:
                    if not client.is_connected():
                        await client.connect()
                        if not await client.is_user_authorized():
                            logger.error("Клиент не авторизован")
                            return

                    async for message in client.iter_messages(chat_id, limit=limit):
                        if not message.media or not isinstance(message.media, MessageMediaDocument):
                            continue
                            
                        if message.media.document.mime_type != 'video/mp4':
                            continue

                        if message.media.document.size > VIDEO_SETTINGS["MAX_FILE_SIZE"]:
                            logger.info(f'Видео {message.id} слишком большое, пропускаем')
                            continue

                        if await video_db_check(message.id):
                            logger.info(f'Видео {message.id} уже существует в базе данных, пропускаем.')
                            continue

                        file_path = os.path.join(folder, f'{message.id}.mp4')
                        try:
                            await download_with_retry(client, message, file_path)
                            await asyncio.sleep(2)  # Добавляем задержку 2 секунды между загрузками
                            if os.path.exists(file_path):
                                await video_db_save(message.id)
                                logger.info(f'Видео загружено и сохранено как {file_path} из чата {chat_id}')
                        except Exception as e:
                            logger.error(f'Ошибка при загрузке видео {message.id}: {str(e)}')
                            if os.path.exists(file_path):
                                os.remove(file_path)
                except Exception as e:
                    logger.error(f'Ошибка при обработке чата {chat_id}: {str(e)}')
    except Exception as e:
        logger.error(f'Критическая ошибка в download_tg_videos: {str(e)}')
    finally:
        await asyncio.sleep(TIMING["UPDATE_INTERVAL"])

async def download_with_retry(client, message, file_path, max_retries=3):
    for attempt in range(max_retries):
        try:
            await client.download_media(message, file_path)
            return True
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f'Ошибка при загрузке видео {message.id} после {max_retries} попыток: {str(e)}')
                return False
            await asyncio.sleep(TIMING["RETRY_DELAY"])

