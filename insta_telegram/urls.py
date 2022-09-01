from django.urls import path
from . import views


urlpatterns = [
    path('webhook/', views.webhook_view, name="telegram_bot_url"),
    path('webhook/remove/', views.remove_webhook, name="remove_telebot_webhook_url"),
]
