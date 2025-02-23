from aiogram import Router, F, types


router = Router()


@router.message(F.text)
async def add_new_domain(message: types.Message):
    try:
        await message.answer("Домен успешно добавлен")
    except Exception as e:
        await message.answer("Произошла ошибка, попробуйте снова отправить ваш домен")
