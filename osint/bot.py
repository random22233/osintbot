import asyncio
import logging
from handlers.start import start_router
from handlers.photo import photo_router
from handlers.email import email_router

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

# async def periodic():
#     while True:
#         print('sdfdsfsdf')
#         await asyncio.sleep(5)
            
async def main() -> None:
    dp = Dispatcher()
    dp.include_routers(
        start_router,
        photo_router,
        email_router,
    )

    # asyncio.create_task(periodic())

    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())