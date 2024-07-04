Project Title

This application - TAVR uses a microservices architecture, featuring a Telegram Bot built with Aiogram3 and a user bot created using Telethon. The project includes two main components:

```TgBot - videoDownload():``` Downloads videos from predefined groups and filters them by topics.

```TgUserBot - videoSend():``` Uploads videos.

Features

Automated Video Downloading: TgBot downloads videos from specific Telegram groups and categorizes them by topics.
Duplicate Prevention: IDs of downloaded videos are stored in an SQLite database to avoid duplicates.
Scheduled Video Uploads: UserTgBot uploads videos from designated folders at specified intervals.
Installation

Clone the repository:

```bash
git clone https://github.com/Adjacentai/TavrBot

cd your-repo-name
```
Install dependencies:

```bash
pip install -r requirements.txt
```
Set up environment variables:

Create a .env file in the root directory.
Add your Telegram API credentials and other necessary configurations:
makefile
```
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
```
Usage

Running TgBot

TgBot is designed to download videos from specific Telegram groups 
and categorize them by topics. 
For example, videos from a group associated with the "FUNNY" category will be saved in the directory ./VideoFolder/Funny. 
The IDs of the downloaded videos are stored in an SQLite database (huita.db) to avoid downloading duplicates.

Run Tavr:
```bash
python tavrBot.py
```
Main File
The main file for this component is tavrBot.py. 
It contains a loop with three asynchronous functions:

```python
while True:
    await asyncio.gather(
        download_tg_videos(client, 100),
        send_my_videos(3000, 'ANIMAL'),
        send_my_videos(3000, 'FUNNY')
        # run if u need to add chat_id in you session.db
        # entity_adding(client)
    )
```
```python
download_tg_videos(client, limit):
#client: Authorization for the UserBot.
#limit: The number of messages to download.

send_my_videos(interval, folder):

#interval: The frequency (in seconds) at which videos are uploaded.
#folder: The folder from which videos are uploaded.
```

