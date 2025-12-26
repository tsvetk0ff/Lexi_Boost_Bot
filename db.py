import aiosqlite
from datetime import datetime

DB_PATH = "bot.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                joined TIMESTAMP,
                score INTEGER DEFAULT 0,
                premium_until TIMESTAMP
            )
        """)
        await db.commit()

async def get_user(telegram_id):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT * FROM users WHERE telegram_id=?", (telegram_id,))
        return await cursor.fetchone()

async def add_user(telegram_id, username, first_name):
    joined = datetime.now()
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (telegram_id, username, first_name, joined) VALUES (?, ?, ?, ?)",
            (telegram_id, username, first_name, joined))
        await db.commit()

async def update_score(telegram_id, delta=1):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE users SET score = score + ? WHERE telegram_id=?", (delta, telegram_id))
        await db.commit()

async def get_top(limit=10):
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT first_name, score FROM users ORDER BY score DESC LIMIT ?", (limit,))
        return await cursor.fetchall()
