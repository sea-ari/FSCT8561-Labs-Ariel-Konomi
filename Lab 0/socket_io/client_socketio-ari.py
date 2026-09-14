
######socket.io

import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('Connection established by Ariel Konomi')

@sio.event
def disconnect():
    print('Ariel disconnected from server')

sio.connect('http://localhost:8080')
sio.emit('message', {'data': 'my_data'})

sio.disconnect()