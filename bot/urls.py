from django.urls import path

from bot.views import start_message

urlpatterns = [
    path('', start_message, name='update'),
]
