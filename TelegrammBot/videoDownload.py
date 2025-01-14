import os
import asyncio
import logging
from DataBase.dbConfig import video_db_check, video_db_save

from telethon.tl.types import MessageMediaDocument
from config import DOWNLOAD_CHANNEL, TIMING


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def download_tg_videos(client, limit: int):
    for chat_ids, folder in DOWNLOAD_CHANNEL.items():
        os.makedirs(folder, exist_ok=True)

        for chat_id in chat_ids:
            async for message in client.iter_messages(chat_id, limit=limit):
                if message.media and isinstance(message.media, MessageMediaDocument):
                    if message.media.document.mime_type == 'video/mp4':
                        if await video_db_check(message.id):
                            logger.info(f'The video {message.id} already exists in the database, skipping it.')
                            continue

                        file_path = os.path.join(folder, f'{message.id}.mp4')
                        try:
                            # Downloading
                            await client.download_media(message, file_path)
                            # Check if video file exists before saving to database
                            if os.path.exists(file_path):
                                try:
                                    await video_db_save(message.id)
                                    logger.info(f'VIDEO DOWNLOADED AND SAVED AS {file_path} FROM CHAT {chat_id}')
                                except Exception as e:
                                    logger.error(f'Error saving video ID to the database. {message.id}: {e}')
                            else:
                                 logger.info(f'VIDEO DOWNLOADED AND SAVED AS {file_path} FROM CHAT {chat_id}')
                        except Exception as e:
                            logger.error('Error while downloading the video {message.id}: {e}')


    await asyncio.sleep(TIMING["UPDATE_INTERVAL"])

