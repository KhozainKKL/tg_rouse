import urllib

import requests
from asgiref.sync import async_to_sync, sync_to_async
from django.http import JsonResponse
from django.shortcuts import render
from django.template import Template, Context
from rest_framework.response import Response
from rest_framework.request import Request
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from rest_framework.views import APIView
from bot.main_bot import bot
from telebot import types

from bot.models import Profile

@bot.message_handler(commands=['start'])
async def start_message(message: Request):
    print(message.from_user.chat.id)
    data = {
        'name': '12333322',
    }
    # URL вашей веб-страницы
    base_url = 'https://khozainkkl.github.io/tg_rouse.github.io/config/static/templates/index.html'

    # # Кодирование данных в формат URL и добавление их к URL веб-страницы
    # encoded_data = urllib.parse.urlencode(data)
    # web_page_url = f'{base_url}?{encoded_data}'

    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton('Открыть веб страницу', web_app=WebAppInfo(
        url=base_url)))
    await bot.send_message(chat_id=message.chat.id, text='Привет.', reply_markup=markup)


@bot.message_handler(func=lambda message: True)
async def start_message(message):
    await bot.send_message(chat_id=message.chat.id, text='Привет, человек.')


def profile_api(request):
    # Получаем данные профиля (например, текущего пользователя)
    profile = Profile.objects.get(user=request.user)
    # Формируем JSON-ответ
    data = {
        'phone': profile.phone,
        # Другие поля профиля, которые вы хотите вернуть
    }
    # Возвращаем ответ в формате JSON
    return JsonResponse(data)
