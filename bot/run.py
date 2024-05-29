import asyncio
import logging

from telebot import util
from telebot.async_telebot import AsyncTeleBot
from environs import Env

from bot.crud import fetch_data

env = Env()
env.read_env()
TG_API_KEY = env.str("TG_API_KEY")
LOGGER_LEVEL = env.str("LOGGER_LEVEL")

logger = logging.getLogger(__name__)

bot = AsyncTeleBot(TG_API_KEY, parse_mode="HTML")


@bot.message_handler(commands=["users", "cart", "order"])
async def echo_message(message):
    result = await fetch_data(message.text, message.from_user.id)
    await bot.send_message(message.chat.id, result)


@bot.message_handler(commands=["products"])
async def echo_message(message):
    result = await fetch_data(message.text)
    await bot.send_message(message.chat.id, result)


if __name__ == "__main__":
    asyncio.run(
        bot.infinity_polling(
            logger_level=LOGGER_LEVEL, allowed_updates=util.update_types
        )
    )
