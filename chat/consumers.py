from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from time import sleep
import asyncio
class ConsumerSync(SyncConsumer):
    def websocket_connect(self, event):
        print("Websocket Sync connected....", event)
        self.send({
            'type': 'websocket.accept'
        })

    def websocket_receive(self, event):
        print("Websocket Sync Received...", event)
        for i in range(20):
            self.send({
                'type': 'websocket.send',
                'text': str(i)
            })
            sleep(1)
    
    def websocket_disconnect(self, event):
        print("Websocket Sync Disconnect...", event)
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