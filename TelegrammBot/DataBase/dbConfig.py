import aiosqlite

DB_PATH = "./DataBase/uita.db"

async def init_db():
    try:
        async with aiosqlite.connect(DB_PATH) as db:
            await db.execute('''CREATE TABLE IF NOT EXISTS Table_Video_id (id INTEGER PRIMARY KEY)''')
            await db.commit()
            print("DB WAS INITIALIZED")
    except aiosqlite.Error as e:
        print(f"Database initialization error: {e}")

async def video_db_check(video_id):
    try:
        async with aiosqlite.connect(DB_PATH) as conn:
            async with conn.execute('SELECT 1 FROM Table_Video_id WHERE id = ?', (video_id,)) as cursor:
                return await cursor.fetchone() is not None
    except aiosqlite.Error as e:
        print(f"Error checking video in the database: {e}")
        return False

async def video_db_save(video_id):

    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute('INSERT INTO Table_Video_id (id) VALUES (?)', (video_id,))
        await conn.commit()
        print(f"ID VIDEO {video_id} ADDed TO DB")


