import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import Message
from webapp.models import Team

#TODO add recencting https://github.com/joewalnes/reconnecting-websocket


class ChatRoomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        # print(self.scope['url_route']['kwargs'])
        self.team_id = self.scope['url_route']['kwargs']['team_id']
        self.chat_room = f'chat_room_{self.team_id}'

        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_room,
            self.channel_name
        )

    # Receive from websocket
    async def receive_json(self, text_data):
        print('receive ', text_data)
        await self.save_text_message(text_data['message'])
        # Send to room group (brodcasts)
        await self.channel_layer.group_send(
            self.chat_room,
            {
                'type': 'chat.message',
                'message': text_data['message'],
                'username': text_data['username']
            }
        )
    
    # Receive message from room group
    async def chat_message(self, event):
        print('chatroom message', event)
        # Send to all websockets
        await self.send_json(content={
            'message': event['message'],
            'username': event['username']
        })
    
    @database_sync_to_async
    def save_text_message(self, message):
        sender = self.user
        team_id = self.team_id

        Message.objects.create(content=message, sender=sender, team_id=team_id)
