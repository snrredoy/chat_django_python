from django.urls import path
from .views import home, room

urlpatterns = [
    path('', home, name='home'),
    path('<str:roomName>/', room, name="room"),
]