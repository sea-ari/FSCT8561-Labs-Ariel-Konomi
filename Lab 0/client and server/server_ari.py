#Part8

import socket

HOST = "127.0.0.1"
PORT = 80

server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Server is waiting for a connection...")

client_socket, client_address = server_socket.accept()

print("Connected by:", client_address)

data = client_socket.recv(1024)

message = data.decode()

print("Client says:", message)

reply = "Server received:" + message


client_socket.send(reply.encode())


client_socket.close() 
#creating a condition of sorts to automatically print that the client disconnected if true
closed = True

match client_socket.close():
    case done if closed:
        print("Client disconnected from the server...")
server_socket.close()