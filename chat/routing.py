from django.urls import path

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:team_id>/', consumers.ChatRoomConsumer.as_asgi()),
]