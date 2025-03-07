from django.shortcuts import render

# Create your views here.
from .models import Room, Message
def index(request):
    sellerRooms = Room.objects.filter(seller=request.user)
    userRooms = Room.objects.filter(user=request.user)

    return render(request, 'chat/index.html', {
        'sellerRooms': sellerRooms,
        'userRooms': userRooms
    })

def room(request, room_name):
    room = Room.objects.get(ID=room_name)
    messages = Message.objects.filter(room=room)
    print("room_name: ", room_name)
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'messages': messages
    })
