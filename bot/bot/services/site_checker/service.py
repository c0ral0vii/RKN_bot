from playwright.async_api import async_playwright, expect
from aiogram import Bot
import asyncio

from bot.services.captcha.service import CaptchaService
from bot.services.database.orm.models_orm import UserORM, DomainORM

class SenderModule:
    async def answer_to_all_users(self, domain, bot: Bot):
        """Отправка уведомления о бане домена"""

        users = await UserORM.get_all_user_id()

        for user in users:
            await bot.send_message(chat_id=user, text=f"Домен был забанен - {domain}")

        await DomainORM.banned_domain(domain)


class SiteCheckerService:
    def __init__(self):
        self.browser = None
        self.page = None
        self.answer_model = SenderModule()
        self.captcha_solver = CaptchaService()

    async def start_browser(self):
        """Запуск браузера и создание новой страницы."""

        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.firefox.launch(headless=True)
        self.page = await self.browser.new_page()

    async def close_browser(self):
        """Закрытие браузера."""

        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    async def check_site(self, domain: str, bot: Bot):
        """Проверка домена на нахождение его в реестре"""

        if not self.page:
            await self.start_browser()

        await self.page.goto("https://eais.rkn.gov.ru/")
        input_field = self.page.locator("input.inputMsg")
        await input_field.fill(domain)

        img_element = self.page.locator("img#captcha_image")
        await img_element.screenshot(path="./image.jpeg")

        input_captcha = self.page.locator("input#captcha")

        captcha_answer = await self.captcha_solver.create_request()
        await input_captcha.fill(captcha_answer)
        print(captcha_answer)
        button = self.page.locator("#send_but2")
        await expect(button).to_be_visible()

        await button.click()
        await asyncio.sleep(2)

        if await self.page.locator(".TblGrid").is_visible():
            await self.answer_model.answer_to_all_users(domain, bot)
        await asyncio.sleep(1)


async def main(bot):
    site_checker = SiteCheckerService()

    try:
        # Запускаем браузер
        await site_checker.start_browser()

        # Пример обработки нескольких IP-адресов
        ip_addresses = await DomainORM.get_all_domain_id()

        for ip in ip_addresses:
            print(f"Проверка IP: {ip}")
            await site_checker.check_site(ip, bot)

    finally:
        # Закрываем браузер после завершения
        await site_checker.close_browser()
