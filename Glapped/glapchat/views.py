from django.shortcuts import render

# Create your views here.
from .models import Room, Message
def index(request):
    # get the rooms where the user is the seller and the buyer
    sellerRooms = Room.objects.filter(seller=request.user)
    buyerRooms = Room.objects.filter(user=request.user)


    return render(request, 'chat/index.html', {
        'sellerRooms': sellerRooms,
        'userRooms': buyerRooms,
        'user' : request.user
    })

def room(request, room_name):
    room = Room.objects.get(ID=room_name)
    messages = Message.objects.filter(room=room)
    if request.user != room.seller and request.user != room.user:
        return render(request, 'chat/forbidden.html', status=403)
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'product': room.product,
        'messages': messages,
        'user' : request.user
    })
    
