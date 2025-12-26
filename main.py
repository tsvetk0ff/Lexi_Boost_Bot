import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from decouple import config
from handlers import router
from db import init_db

TOKEN = config('BOT_TOKEN')

async def main():
    await init_db()
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)
    print("🚀 Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
