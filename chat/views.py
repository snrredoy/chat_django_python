from django.shortcuts import render
from .models import Chat, Group

# Create your views here.
def home(request):
    return render(request, 'chat/index.html')

def room(request, roomName):
    user = request.user
    chats = []
    room = Group.objects.filter(name=roomName).first()
    if not room:
        Group.objects.create(name = roomName)
    
    if user.is_authenticated:
        room.member.add(user)

    chats = Chat.objects.filter(group=room)

    context = {
        'roomName': roomName,
        'chats': chats
    }
    return render(request, 'chat/room.html', context=context)