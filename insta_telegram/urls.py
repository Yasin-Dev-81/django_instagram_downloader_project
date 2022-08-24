from .views import webhook_view
from django.urls import path


urlpatterns = [
    path('webhook/', webhook_view, name="telegram_bot_url"),
]
