from django.urls import path

from bot.views import UpdateBot, profile_api

urlpatterns = [
    path('', UpdateBot.as_view(), name='update'),
    path('api/profile/', profile_api, name='profile_api'),
]
