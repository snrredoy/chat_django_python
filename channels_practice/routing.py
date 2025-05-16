from django.urls import path
from channels_practice.consumers import ConsumerSync, ConsumerAsync

websocket_urlpatterns = [
    path('wc/sc/', ConsumerSync.as_asgi()),
    path('wc/ac/', ConsumerAsync.as_asgi()),
]