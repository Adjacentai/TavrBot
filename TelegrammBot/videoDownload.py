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
            logger.info(f"Начинаем проверку видео в папке: {folder}")
            os.makedirs(folder, exist_ok=True)

            for chat_id in chat_ids:
                try:
                    if not client.is_connected():
                        await client.connect()
                        if not await client.is_user_authorized():
                            logger.error("Клиент не авторизован")
                            return

                    logger.info(f"Проверяем канал с ID: {chat_id}")
                    async for message in client.iter_messages(chat_id, limit=limit):
                        if not message.media or not isinstance(message.media, MessageMediaDocument):
                            continue
                            
                        if message.media.document.mime_type != 'video/mp4':
                            continue

                        if message.media.document.size > VIDEO_SETTINGS["MAX_FILE_SIZE"]:
                            logger.info(f'Видео {message.id} из канала {chat_id} слишком большое ({message.media.document.size} байт), пропускаем')
                            continue

                        if await video_db_check(message.id):
                            logger.info(f'Видео {message.id} уже существует в базе данных, пропускаем.')
                            continue

                        file_path = os.path.join(folder, f'{message.id}.mp4')
                        logger.info(f"Начинаем загрузку видео {message.id} из канала {chat_id} в {folder}")
                        
                        try:
                            await download_with_retry(client, message, file_path)
                            # Используем значение по умолчанию, если ключ отсутствует
                            delay = TIMING.get("VIDEO_DOWNLOAD_DELAY", 30)
                            await asyncio.sleep(delay)
                            if os.path.exists(file_path):
                                await video_db_save(message.id)
                                file_size = os.path.getsize(file_path)
                                logger.info(f'Видео {message.id} успешно загружено в {folder}. Размер: {file_size} байт')
                        except Exception as e:
                            logger.error(f'Ошибка при загрузке видео {message.id} из канала {chat_id}: {str(e)}')
                            await asyncio.sleep(TIMING["RETRY_DELAY"])
                except Exception as e:
                    logger.error(f'Ошибка при обработке канала {chat_id}: {str(e)}')
                    await asyncio.sleep(TIMING["RETRY_DELAY"])
    except Exception as e:
        logger.error(f'Критическая ошибка в download_tg_videos: {str(e)}')
    finally:
        await asyncio.sleep(TIMING["UPDATE_INTERVAL"])

async def download_with_retry(client, message, file_path, max_retries=3):
    temp_path = f"{file_path}.temp"
    for attempt in range(max_retries):
        try:
            # Удаляем временный файл, если он существует
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            # Загружаем во временный файл
            await client.download_media(message, temp_path)
            
            # Ждем немного, чтобы убедиться, что файл полностью записан
            await asyncio.sleep(29)
            
            # Проверяем размер загруженного файла
            if os.path.exists(temp_path):
                file_size = os.path.getsize(temp_path)
                if file_size > 0 and file_size == message.media.document.size:
                    # Если размер совпадает с ожидаемым, переименовываем
                    os.rename(temp_path, file_path)
                    return True
                else:
                    logger.error(f"Размер файла не совпадает: ожидалось {message.media.document.size}, получено {file_size}")
                    os.remove(temp_path)
            else:
                raise Exception("Файл не был создан")
                
        except Exception as e:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            if attempt == max_retries - 1:
                logger.error(f'Ошибка при загрузке видео {message.id} после {max_retries} попыток: {str(e)}')
                return False
            logger.info(f'Попытка {attempt + 1} не удалась, ожидание перед следующей попыткой')
            await asyncio.sleep(TIMING["RETRY_DELAY"])

