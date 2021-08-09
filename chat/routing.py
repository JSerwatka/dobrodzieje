from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('chat/<str:team_id>/', consumers.ChatRoomConsumer.as_asgi()),
]