import asyncio
import logging

import pytz
from aiogram import Bot, Dispatcher, types
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from bot.services.site_checker.service import main as check_site_main
from bot.services.core.config.config import options
from bot.handlers import start_handler, add_new_domain


bot = Bot(token=options.BOT_API)
dp = Dispatcher()

dp.include_routers(
    start_handler.router,
    add_new_domain.router,
)


async def run_workers():
    """Запуск воркеров для работы над проверкой доменов каждые 30 минут"""
    # await check_site_main(bot)

    logger.debug("Запускаем воркеры")
    scheduler = AsyncIOScheduler(timezone=pytz.timezone("Europe/Moscow"))

    scheduler.add_job(check_site_main, "interval", minutes=1, args=[bot])
    scheduler.start()


async def on_startup():
    """Код который выполняется при запуске"""

    commands = [
        types.BotCommand(command="/start", description="Запуск бота"),
    ]
    await bot.set_my_commands(commands)


async def main():
    """Запуск бота"""
    await run_workers()
    logger.debug("Запускаем")
    await bot.delete_webhook(drop_pending_updates=True)
    await on_startup()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Создаем обработчик для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # Создаем форматтер
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    # Добавляем обработчик к логгеру
    logger.addHandler(console_handler)
    asyncio.run(main())
