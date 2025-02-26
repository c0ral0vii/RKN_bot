import asyncio

import pytz
from aiogram import Bot, Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.services.site_checker.service import main
from bot.services.core.config.config import options
from bot.handlers import (
    start_handler,
    add_new_domain
)

bot = Bot(token=options.BOT_API)
dp = Dispatcher()

dp.include_routers(
    start_handler.router,
    add_new_domain.router,
)

async def run_workers():
    """Запуск воркеров для работы над проверкой доменов каждые 30 минут"""

    scheduler = AsyncIOScheduler(timezone=pytz.timezone("Europe/Moscow"))
    scheduler.add_job(main, 'interval', seconds=30)
    scheduler.start()

async def on_startup():
    """Код который выполняется при запуске"""
    await run_workers()

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