from aiogram import Dispatcher
from app.handlers.user import user_router
from app.database.models import start_db
from bot import bot
import asyncio

async def main():
    start_db
    dp = Dispatcher()
    dp.include_router(user_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())