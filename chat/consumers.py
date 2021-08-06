import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class ChatRoomConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
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