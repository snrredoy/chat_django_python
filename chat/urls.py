from django.urls import path
from .views import home, room

urlpatterns = [
    # path('', home, name='home'),
    path("", room, name="room"),
]