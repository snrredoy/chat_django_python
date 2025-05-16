from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from time import sleep
import asyncio
class ConsumerSync(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket Sync connected....", event)
        print("Channel layer...", [self.channel_layer])
        print("Channel name...", [self.channel_name])
        async_to_sync(self.channel_layer.group_add)(
            'p',
            self.channel_name
        )
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print("Websocket Sync Received...", event['text'])
        async_to_sync(self.channel_layer.group_send)(
            'p',
            {
                'type': 'chat.message',
                'message': event['text']
            }
        )
    
    def chat_message(self, event):
        msg = event['message']
        self.send({
            'type': 'websocket.send',
            'text': event['message']
        })
    
    def websocket_disconnect(self, event):
        print("Websocket Sync Disconnect...", event)
        print("Channel layer...", [self.channel_layer])
        print("Channel name...", [self.channel_name])
        async_to_sync(self.channel_layer.group_discard)(
            'p',
            self.channel_name,
        )
        raise StopConsumer()
    
class ConsumerAsync(AsyncConsumer):
    async def websocket_connect(self, event):
        print('Websocket Async connect...', event)
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        print('Websocket Async receive...', event)
        for i in range(20):
            await self.send({
                'type': 'websocket.send',
                'text': str(i)
            })
            await asyncio.sleep(1)

    async def websocket_disconnect(self, event):
        print('Websocket Async disconnect...', event)
        raise StopConsumer()