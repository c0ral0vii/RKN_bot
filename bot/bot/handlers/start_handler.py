from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()

START_MESSAGE = "Отправьте ссылку на домен который необходимо отслеживать"


@router.message(CommandStart)
async def start_handler(message: types.Message):
    await message.answer(START_MESSAGE)
