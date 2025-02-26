import asyncio

from aiogram import Bot, Dispatcher, types
from bot.services.core.config.config import options
from bot.handlers import (
    start_handler,
    add_new_domain
)

bot = Bot(token=options.BOT_API)
dp = Dispatcher()

dp.include_routers(
    start_handler.router,
)

async def on_startup():
    """Код который выполняется при запуске"""

    commands = [
        types.BotCommand(command="/start", description="Запуск бота"),
    ]
    await bot.set_my_commands(commands)

async def main():
    """Запуск бота"""

    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())