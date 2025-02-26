from aiogram import Router, types
from aiogram.filters import CommandStart
from bot.bot.services.database.orm.models_orm import UserORM


router = Router()

START_MESSAGE = "Отправьте ссылку на домен который необходимо отслеживать"


@router.message(CommandStart)
async def start_handler(message: types.Message):
    await UserORM.create_user(message.from_user.id)
    await message.answer(START_MESSAGE)
