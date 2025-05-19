from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from time import sleep
import asyncio
from .models import Group, Chat
import json
class ConsumerSync(SyncConsumer):
    def websocket_connect(self, event):
        self.roomName = self.scope['url_route']['kwargs']['roomName']
        async_to_sync(self.channel_layer.group_add)(
            self.roomName,
            self.channel_name
        )
        self.send({
            'type': 'websocket.accept'
        })

    # def websocket_receive(self, event):
    #     data = json.loads(event['text'])
    #     room = Group.objects.get(name = self.roomName)
    #     if self.scope['user'].is_authenticated:
    #         Chat.objects.create(
    #             sender = self.scope['user'],
    #             content = data['message'],
    #             group = room
    #         )
    #         async_to_sync(self.channel_layer.group_send)(
    #             self.roomName,
    #             {
    #                 'type': 'chat.message',
    #                 'message': event['text'],
    #                 'full_name': f'{self.scope['user'].first_name} {self.scope['user'].last_name}'
    #             }
    #         )
    #     else:
    #         self.send({
    #             'type' : 'websocket.send',
    #             'text': json.dumps({
    #                 'message': 'Login Required'
    #                 })
    #         })
    
    # def chat_message(self, event):
    #     msg = event['message']
    #     self.send({
    #         'type': 'websocket.send',
    #         'text': json.dumps({
    #             'message': event['message'],
    #             'full_name': event['full_name']
    #         })
    #     })
    
    def websocket_receive(self, event):
        data = json.loads(event['text'])
        room = Group.objects.get(name=self.roomName)
        if self.scope['user'].is_authenticated:
            chat = Chat.objects.create(
                sender=self.scope['user'],
                content=data['message'],
                group=room
            )
            full_name = f"{self.scope['user'].first_name} {self.scope['user'].last_name}".strip() or self.scope['user'].username
            async_to_sync(self.channel_layer.group_send)(
                self.roomName,
                {
                    'type': 'chat.message',
                    'message': data['message'],
                    'username': self.scope['user'].username,
                    'full_name': full_name,
                    'created_at': chat.created_at.isoformat()  # Send the creation timestamp
                }
            )
        else:
            self.send({
                'type': 'websocket.send',
                'text': json.dumps({'message': 'Login Required'})
            })
    
    def chat_message(self, event):
        self.send({
            'type': 'websocket.send',
            'text': json.dumps({
                'message': event['message'],
                'username': event['username'],
                'full_name': event['full_name'],
                'created_at': event['created_at']
            })
        })



    def websocket_disconnect(self, event):
        async_to_sync(self.channel_layer.group_discard)(
            self.roomName,
            self.channel_name,
        )
        raise StopConsumer()
    
class ConsumerAsync(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        for i in range(20):
            await self.send({
                'type': 'websocket.send',
                'text': str(i)
            })
            await asyncio.sleep(1)

    async def websocket_disconnect(self, event):
        raise StopConsumer()