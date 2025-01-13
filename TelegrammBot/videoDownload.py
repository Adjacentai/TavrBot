import os
import asyncio
from DataBase.dbConfig import video_db_check, video_db_save
from telethon.tl.types import MessageMediaDocument
from config import DOWNLOAD_CHANNEL
from logger_config import setup_logger

# Настраиваем логгер для этого модуля
logger = setup_logger('video_downloader')

async def download_tg_videos(client, limit: int):
    """
    Загружает видео из Telegram каналов
    
    Args:
        client: Telegram клиент
        limit (int): Максимальное количество сообщений для обработки
    """
    for chat_ids, folder in DOWNLOAD_CHANNEL.items():
        os.makedirs(folder, exist_ok=True)
        logger.info(f"Начинаю обработку папки: {folder}")

        for chat_id in chat_ids:
            logger.info(f"Обработка чата: {chat_id}")
            try:
                async for message in client.iter_messages(chat_id, limit=limit):
                    if message.media and isinstance(message.media, MessageMediaDocument):
                        if message.media.document.mime_type == 'video/mp4':
                            if await video_db_check(message.id):
                                logger.debug(f'Видео {message.id} уже существует в базе данных, пропускаю.')
                                continue

                            file_path = os.path.join(folder, f'{message.id}.mp4')
                            try:
                                await client.download_media(message, file_path)
                                if os.path.exists(file_path):
                                    try:
                                        await video_db_save(message.id)
                                        logger.info(f'Видео успешно загружено и сохранено: {file_path} из чата {chat_id}')
                                    except Exception as e:
                                        logger.error(f'Ошибка сохранения ID видео в базе данных {message.id}: {str(e)}')
                                else:
                                    logger.warning(f'Файл не найден после загрузки: {file_path}')
                            except Exception as e:
                                logger.error(f'Ошибка при загрузке видео {message.id}: {str(e)}')
            except Exception as e:
                logger.error(f'Ошибка при обработке чата {chat_id}: {str(e)}')

    logger.info("Завершение цикла загрузки, ожидание следующего цикла")
    await asyncio.sleep(86600)

async def entity_adding(client):
    """Добавляет новые сущности чатов в сессию"""
    logger.info("Начало добавления сущностей")
    try:
        async with client:
            dialogs = await client.get_dialogs()
            for dialog in dialogs:
                try:
                    entity = await client.get_entity(dialog.id)
                    logger.info(f"Добавлена сущность: {entity}")
                except Exception as e:
                    logger.error(f"Ошибка при получении сущности для диалога {dialog.id}: {str(e)}")
    except Exception as e:
        logger.error(f"Ошибка при добавлении сущностей: {str(e)}")
    logger.info("Завершение добавления сущностей")