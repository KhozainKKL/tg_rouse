import telebot
from django.conf import settings
from telebot.async_telebot import AsyncTeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

bot = AsyncTeleBot(settings.TG_API_KEY, parse_mode='HTML')
telebot.logger.setLevel(settings.LOGLEVEL)


@bot.message_handler(commands=['start'])
async def echo_mes(message):
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton('Открыть веб страницу', web_app=WebAppInfo(
        url='https://htmlpreview.github.io/?https://github.com/KhozainKKL/tg_rouse/blob/main/config/templates/index.html')))
    await bot.send_message(chat_id=message.chat.id, text='Привет.', reply_markup=markup)
