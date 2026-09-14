#######SOCKET.IO

from aiohttp import web
import socketio

socket_io = socketio.AsyncServer()
app = web.Application()
socket_io.attach(app)

async def index(request):
    return web.Response(text='Hello world from Ariel Konomi',content_type='text/html')

@socket_io.on('message')
def print_message(socket_id,data):
    print("Socket ID: " , socket_id)
    print("Data: " , data)

sio = socketio.Client()
sio.disconnect() 
#creating a condition of sorts to automatically print that the client disconnected if true
closed = True

match sio.disconnect():
    case done if closed:
        print("Client disconnected from the server...")



app.router.add_get('/', index)

if __name__ == '__main__':
    web.run_app(app)

