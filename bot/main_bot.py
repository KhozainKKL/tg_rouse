import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


# @bot.message_handler(commands=['start'])
# async def echo_mes(message):
#     markup = ReplyKeyboardMarkup()
#     markup.add(KeyboardButton('Открыть веб страницу', web_app=WebAppInfo(
#         url='https://htmlpreview.github.io/?https://github.com/KhozainKKL/tg_rouse/blob/main/config/static/templates/index.html')))
#     await bot.send_message(chat_id=message.chat.id, text='Привет.', reply_markup=markup)
