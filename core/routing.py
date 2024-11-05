from django.urls import path
from .consumer import *

websocket_urlpatterns = [
    path('ws/chats/<int:room_id>/', ChatConsumer.as_asgi()),
]