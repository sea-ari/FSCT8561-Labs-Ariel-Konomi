
######socket.io

import socketio

sio = socketio.Client()


@sio.event
def connect():
    print('Connection established by Ariel Konomi')

print()

sio.connect('http://localhost:8080')

while True:
    msg = input("Type a message (or EXIT to quit): ")
    if msg == "EXIT":
        break
    
    sio.emit("message", msg)

print()

@sio.event
def disconnect():
    print('Ariel disconnected from server')


sio.disconnect()