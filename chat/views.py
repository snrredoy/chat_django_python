from django.shortcuts import render
from .models import Chat, Group

# Create your views here.
def home(request):
    return render(request, 'chat/index.html')

def room(request, roomName):
    chats = []
    room = Group.objects.filter(name=roomName).first()
    if room:
        chats = Chat.objects.filter(group=room)
    else:
        Group.objects.create(
            name = roomName
        )

    context = {
        'roomName': roomName,
        'chats': chats
    }
    return render(request, 'chat/room.html', context=context)