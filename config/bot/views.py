from django.http import JsonResponse
from django.shortcuts import render
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from rest_framework.views import APIView

from bot.main_bot import bot
from telebot import types

from bot.models import Profile


class UpdateBot(APIView):
    def post(self, request):
        json_str = request.body.decode('UTF-8')
        update = types.Update.de_json(json_str)
        bot.process_new_updates([update])


@bot.message_handler(commands=['start'])
async def start_message(message):
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton('Открыть веб страницу', web_app=WebAppInfo(
        url='https://khozainkkl.github.io/tg_rouse.github.io/config/static/templates/index.html')))
    await bot.send_message(chat_id=message.chat.id, text='Привет.', reply_markup=markup)


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
