from environs import Env


from bot.crud import DatabaseRequestToBot as db

from bot.run import bot


# @bot.message_handler(func=lambda message: True)
# async def start_message(message):
#     await bot.send_message(chat_id=message.chat.id, text="Привет, человек.")
