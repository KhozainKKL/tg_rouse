import asyncio
import logging
import json
import urllib
from telebot import util
from telebot.async_telebot import AsyncTeleBot
from environs import Env
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from bot.crud import DatabaseRequestToBot as db

env = Env()
env.read_env()
TG_API_KEY = env.str("TG_API_KEY")
LOGGER_LEVEL = env.str("LOGGER_LEVEL")

logger = logging.getLogger(__name__)

bot = AsyncTeleBot(TG_API_KEY, parse_mode="HTML")

BASE_URL = env.str("BASE_URL")


@bot.message_handler(commands=["login"])
async def start_message(message):

    # Кодирование данных в формат URL и добавление их к URL веб-страницы
    web_page_url = BASE_URL + "auth.html"

    markup = ReplyKeyboardMarkup()
    markup.add(
        KeyboardButton("Открыть веб страницу", web_app=WebAppInfo(url=web_page_url))
    )
    await bot.send_message(chat_id=message.chat.id, text="Привет.", reply_markup=markup)


@bot.message_handler(commands=["cart"])
async def cart(message):
    encoded_data = urllib.parse.quote(
        json.dumps(
            await db.get_fetch_data(url_template="cart", data_id=message.from_user.id)
        )
    )
    url = BASE_URL + f"cart.html?product={encoded_data}"
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton("Корзина 🧺", web_app=WebAppInfo(url=url)))
    await bot.send_message(chat_id=message.chat.id, text="Привет.", reply_markup=markup)


@bot.message_handler(commands=["users", "order"])
async def echo_message(message):
    result = await db.get_fetch_data(message.text, message.from_user.id)
    await bot.send_message(message.chat.id, result)


@bot.message_handler(commands=["products"])
async def echo_message(message):
    result = await db.get_fetch_data(message.text)
    await bot.send_message(message.chat.id, result)


@bot.message_handler(commands=["search"])
async def search_product(message):
    products = await db.get_fetch_data(message.text)
    encoded_sort = urllib.parse.quote(json.dumps(products))

    url = BASE_URL + f"search.html?product={encoded_sort}"
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton("Поиск товара 🔎", web_app=WebAppInfo(url=url)))
    await bot.send_message(chat_id=message.chat.id, text="Привет.", reply_markup=markup)

    @bot.message_handler(content_types=["web_app_data"])
    async def result_search_product(message):
        prod = await db.get_search_product(data=json.loads(message.web_app_data.data))
        if not prod:
            await bot.send_message(chat_id=message.chat.id, text="Товар не найден.")
        if prod:
            keyb_list_search_prod = InlineKeyboardMarkup()
            print(prod)
            for item in prod:
                keyb_list_search_prod.add(
                    InlineKeyboardButton(
                        text=f'{item["name"]}', callback_data=f'data_{item["name"]}'
                    )
                )

            await bot.send_message(
                chat_id=message.chat.id,
                text="Найденные товары",
                reply_markup=keyb_list_search_prod,
            )

            @bot.callback_query_handler(lambda query: query.data.startswith("data_"))
            async def post_details_search_product(query):
                date = query.data.split("_")[1]
                keyb_details_product = InlineKeyboardMarkup(row_width=1)
                keyb_details_product.add(
                    InlineKeyboardButton("Добавить в корзину 🧺", callback_data="2"),
                    InlineKeyboardButton(
                        "Назад", callback_data="back_to_list_search_product"
                    ),
                )
                for items in prod:
                    if items["name"] == date:
                        text = (
                            f'Название: {items["name"]}\n'
                            f'Описание: {items["description"]}\n'
                            f'Цена: {items["price"]}\n'
                            f'<a href="https://khozainkkl.github.io/tg_rouse.github.io/tg_rouse/media/{items["image"]}"> </a>'
                        )
                await bot.edit_message_text(
                    chat_id=query.message.chat.id,
                    text=text,
                    message_id=query.message.message_id,
                    reply_markup=keyb_details_product,
                )

                @bot.callback_query_handler(
                    func=lambda call: call.data == "back_to_list_search_product"
                )
                async def back_to_list_search_product(call):
                    await bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        text="Найденные товары",
                        message_id=call.message.message_id,
                        reply_markup=keyb_list_search_prod,
                    )


if __name__ == "__main__":
    asyncio.run(
        bot.infinity_polling(
            logger_level=LOGGER_LEVEL, allowed_updates=util.update_types
        )
    )
