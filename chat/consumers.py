import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import Message
from webapp.models import Team

@database_sync_to_async
def save_text_message(message, sender, team_id):
    Message.objects.create(content=message, sender=sender, team_id=team_id)


class ChatRoomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        # print(self.scope['url_route']['kwargs'])
        self.team_id = self.scope['url_route']['kwargs']['team_id']
        self.room_group_name = f'chat_team_{self.team_id}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive from websocket
    async def receive_json(self, text_data):
        await save_text_message(text_data['message'], self.user, self.team_id)
        # Send to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chatroom_message',
                'message': text_data['message'],
                'username': text_data['username']
            }
        )
    
    # Receive message from room group
    async def chatroom_message(self, event):
        await self.send_json(content={
            'message': event['message'],
            'username': event['username']
        })