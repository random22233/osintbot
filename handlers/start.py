from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

start_router = Router()

@start_router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Hello, <b>{message.from_user.full_name}!</b>\n send an email or photo to start")