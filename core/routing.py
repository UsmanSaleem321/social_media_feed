from django.urls import path
from core.consumer import ChatConsumer


websocket_urlpatterns = [
    path('ws/chats/<int:room_id>/', ChatConsumer.as_asgi()),
]