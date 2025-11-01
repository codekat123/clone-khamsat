from django.urls import path
from chat.routing import websocket_urlpatterns as chat_ws

websocket_urlpatterns = [
    *chat_ws,
]

