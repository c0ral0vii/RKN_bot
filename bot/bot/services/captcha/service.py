import asyncio

import aiohttp
import base64


class CaptchaService:
    def __init__(self):
        self.type = ""
        self.url_create = "http://api.cap.guru/in.php"
        self.url_result = "http://api.cap.guru/res.php"
        self.key = "8dca79986843e11e5f89308bbbe749f8"

        self.header = {
            "Content-Type": "application/json",
        }

    async def create_request(self):
        async with aiohttp.ClientSession() as session:
            with open(
                "./image.jpeg",
                "rb",
            ) as file:
                file_content = file.read()
                IMAGE_BASE_64 = base64.b64encode(file_content).decode("utf-8")

            data = {
                "key": self.key,
                "method": "base64",
                "body": IMAGE_BASE_64,
                "json": 1,
            }

            request = await session.post(
                self.url_create, headers=self.header, json=data
            )

            request = await request.json()
            print(request)
            if request["status"] == 1:
                task_id = request["request"]
                await asyncio.sleep(12)
                captcha_answer = await self.get_result(task_id, session)

                return captcha_answer

    async def get_result(self, task_id, session):
        data = {
            "key": self.key,
            "action": "get",
            "id": task_id,
            "json": 1,
        }

        request = await session.post(self.url_result, headers=self.header, json=data)
        request.raise_for_status()
        request = await request.json()

        if request["status"] == 1:
            return request["request"]
        if request["status"] == 0 and request["request"] != "CAPCHA_NOT_READY":
            await asyncio.sleep(2)
            print(task_id)
            await self.get_result(task_id, session)
