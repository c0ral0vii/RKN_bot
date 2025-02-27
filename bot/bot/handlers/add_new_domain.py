from aiogram import Router, F, types
from aiogram.types import InlineKeyboardButton

from bot.services.database.orm.models_orm import DomainORM, UserORM

router = Router()


@router.message(F.text)
async def add_new_domain(message: types.Message):
    try:
        await message.answer(
            f"Вы уверены в добавлении домена - {message.text} \n Если вы ввели домен не правильно просто не нажимайте кнопку снизу!",
            reply_markup=types.InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Подтвердить вставку",
                            callback_data=f"add_{message.text}",
                        )
                    ]
                ]
            ),
        )
    except Exception as e:
        await message.answer("Произошла ошибка, попробуйте снова отправить ваш домен")


@router.callback_query(F.data.startswith("add_"))
async def add_new_domain_callback(query: types.CallbackQuery):
    await DomainORM.create_domain(query.data.replace("add_", ""))
    await query.message.delete()
    await query.message.answer("Домен успешно добавлен")
