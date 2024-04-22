import telebot
from django.conf import settings
from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot(settings.TG_API_KEY, parse_mode='HTML')
telebot.logger.setLevel(settings.LOGLEVEL)


@bot.message_handler(commands=['start'])
async def echo_mes(message):
    await bot.send_message(chat_id=message.chat.id, text='Привет.')
