from asgiref.sync import async_to_sync, sync_to_async
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from rest_framework.views import APIView
from bot.main_bot import bot
from telebot import types

from bot.models import Profile


@sync_to_async
def thread():
    profile = Profile.objects.get(id=1)
    return profile


@bot.message_handler(commands=['start'])
async def start_message(message: Request):
    data = {
        'name': await thread(),
    }
    result = render(message, 'https://khozainkkl.github.io/tg_rouse.github.io/config/static/templates/index.html',
                    context=data)
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton('Открыть веб страницу', web_app=WebAppInfo(
        url=result)))
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
