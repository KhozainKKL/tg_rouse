import json
import urllib

import requests
from asgiref.sync import async_to_sync, sync_to_async
from django.http import JsonResponse
from django.shortcuts import render
from django.template import Template, Context
from rest_framework.response import Response
from rest_framework.request import Request
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from rest_framework.views import APIView
from bot.main_bot import bot
from telebot import types

from config.database.response_bot import DatabaseRequestToBot as db


@bot.message_handler(commands=['start'])
async def start_message(message):
    data = {
        'name': await db.get_all_product(),
    }
    # URL вашей веб-страницы
    base_url = 'https://khozainkkl.github.io/tg_rouse.github.io/config/static/templates/index.html'
    # Кодирование данных в формат URL и добавление их к URL веб-страницы
    encoded_data = urllib.parse.urlencode(data)
    web_page_url = f'{base_url}?{encoded_data}'

    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton('Открыть веб страницу', web_app=WebAppInfo(
        url=web_page_url)))
    await bot.send_message(chat_id=message.chat.id, text='Привет.', reply_markup=markup)


@bot.message_handler(commands=['cart'])
async def cart(message):
    encoded_data = urllib.parse.quote(json.dumps(await db.get_all_product()))
    url = f"https://khozainkkl.github.io/tg_rouse.github.io/config/static/templates/cart.html?product={encoded_data}"
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton('Корзина 🧺', web_app=WebAppInfo(
        url=url)))
    await bot.send_message(chat_id=message.chat.id, text='Привет.', reply_markup=markup)

    # @bot.message_handler(content_types=['web_app_data'])
    # async def ordering_complete_cart(message):
    #     prod = json.loads(message.web_app_data.data)
    #
    #     await bot.send_message(chat_id=message.chat.id, text=prod)


@bot.message_handler(commands=['search'])
async def search_product(message):
    products = await db.post_search_product()
    encoded_sort = urllib.parse.quote(json.dumps(products))

    url = (
        f"https://khozainkkl.github.io/tg_rouse.github.io/config/static/templates/search.html?product={encoded_sort}")
    markup = ReplyKeyboardMarkup()
    markup.add(KeyboardButton('Поиск товара 🔎', web_app=WebAppInfo(
        url=url)))
    await bot.send_message(chat_id=message.chat.id, text='Привет.', reply_markup=markup)

    @bot.message_handler(content_types=['web_app_data'])
    async def result_search_product(message: Request):
        prod = await db.get_search_product(data=json.loads(message.web_app_data.data))
        if not prod:
            await bot.send_message(chat_id=message.chat.id, text='Товар не найден.')
        if prod:
            keyb_list_search_prod = InlineKeyboardMarkup()
            print(prod)
            for item in prod:
                keyb_list_search_prod.add(
                    InlineKeyboardButton(text=f'{item["name"]}', callback_data=f'data_{item["name"]}'))

            await bot.send_message(chat_id=message.chat.id, text='Найденные товары',
                                   reply_markup=keyb_list_search_prod)

            @bot.callback_query_handler(lambda query: query.data.startswith('data_'))
            async def post_details_search_product(query):
                date = query.data.split('_')[1]
                keyb_details_product = InlineKeyboardMarkup(row_width=1)
                keyb_details_product.add(InlineKeyboardButton('Добавить в корзину 🧺', callback_data='2'),
                                         InlineKeyboardButton('Назад', callback_data='back_to_list_search_product')
                                         )
                for items in prod:
                    if items['name'] == date:
                        text = (f'Название: {items["name"]}\n'
                                f'Описание: {items["description"]}\n'
                                f'Цена: {items["price"]}\n'
                                f'<a href="https://khozainkkl.github.io/tg_rouse.github.io/config/media/{items["image"]}"> </a>')
                await bot.edit_message_text(chat_id=query.message.chat.id, text=text,
                                            message_id=query.message.message_id,
                                            reply_markup=keyb_details_product)

                @bot.callback_query_handler(func=lambda call: call.data == "back_to_list_search_product")
                async def back_to_list_search_product(call):
                    await bot.edit_message_text(chat_id=call.message.chat.id, text='Найденные товары',
                                                message_id=call.message.message_id, reply_markup=keyb_list_search_prod)


@bot.message_handler(func=lambda message: True)
async def start_message(message):
    await bot.send_message(chat_id=message.chat.id, text='Привет, человек.')
