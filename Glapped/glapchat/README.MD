to make glapchat work on the server end:
change room.html 

add the s:

const chatSocket = new WebSocket(
            'wss://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/'
        );

run this command in the terminal:

daphne -b 0.0.0.0 -p 8001 Glapped.asgi:application