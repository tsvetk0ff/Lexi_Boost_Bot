import sqlite3
from datetime import datetime
import threading

DB_PATH = "bot.db"
lock = threading.Lock()

def init_db():
    with lock:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                joined TIMESTAMP,
                score INTEGER DEFAULT 0,
                premium_until TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

def get_user(telegram_id):
    with lock:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute("SELECT * FROM users WHERE telegram_id=?", (telegram_id,))
        result = cursor.fetchone()
        conn.close()
        return result

def add_user(telegram_id, username, first_name):
    with lock:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT OR IGNORE INTO users (telegram_id, username, first_name, joined) VALUES (?, ?, ?, ?)",
            (telegram_id, username, first_name, datetime.now())
        )
        conn.commit()
        conn.close()

def update_score(telegram_id, delta=1):
    with lock:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("UPDATE users SET score = score + ? WHERE telegram_id=?", (delta, telegram_id))
        conn.commit()
        conn.close()

def get_top(limit=10):
    with lock:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.execute(
            "SELECT first_name, score FROM users ORDER BY score DESC LIMIT ?", (limit,)
        )
        result = cursor.fetchall()
        conn.close()
        return result
