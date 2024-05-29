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


# Функция для получения данных из FastAPI
async def fetch_data(data, data_id=None):
    if not data_id:
        async with aiohttp.ClientSession() as session:
            async with session.get(API + f"{data}/") as response:
                return await response.json()
    else:
        async with aiohttp.ClientSession() as session:
            async with session.get(API + f"{data}/{data_id}/") as response:
                return await response.json()
