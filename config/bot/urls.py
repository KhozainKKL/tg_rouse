from django.urls import path

from bot.views import start_message, profile_api

urlpatterns = [
    path('', start_message, name='update'),
    path('api/profile/', profile_api, name='profile_api'),
]
