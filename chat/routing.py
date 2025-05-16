from django.urls import path
from chat.consumers import ConsumerSync, ConsumerAsync

websocket_urlpatterns = [
    path('ws/sc/<str:roomName>/', ConsumerSync.as_asgi()),
    path('ws/ac/<str:roomName>/', ConsumerAsync.as_asgi()),
]