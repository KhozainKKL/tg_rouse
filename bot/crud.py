"""
Create
Read
Update
Delete
"""

import aiohttp
from environs import Env

env = Env()
env.read_env()
API = env.str("API")


class DatabaseRequestToBot:
    # Функция для получения данных из FastAPI
    @staticmethod
    async def get_fetch_data(url_template: str, data_id: int = None):
        async with aiohttp.ClientSession() as session:
            if not data_id:
                async with session.get(API + f"{url_template}/") as response:
                    return await response.json()
            else:
                async with session.get(API + f"{url_template}/{data_id}/") as response:
                    return await response.json()
