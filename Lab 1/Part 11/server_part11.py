#######SOCKET.IO

from aiohttp import web
import socketio

sio= socketio.AsyncServer()
app = web.Application()
sio.attach(app)

@sio.on('message')
def print_message(socket_id,data):
    print("Socket ID: " , socket_id)
    print("Data: " , data)
print()
print()
# Stateful tracking: Keep a list of active users
active_users = set()

@sio.event
async def connect(sid, environ):
    active_users.add(sid)
    print(f"Client connected: {sid}")

print()

@sio.on('message')
async def handle_message(sid, data):
    print(f"Received from {sid}: {data}")
    # Echo back to the specific client
    await sio.emit('reply', f"Server received: {data}", to=sid)

print()

@sio.event
async def disconnect(sid):
    active_users.remove(sid)
    print(f"Client disconnected: {sid}")

if __name__ == '__main__':
    web.run_app(app, port=8080)