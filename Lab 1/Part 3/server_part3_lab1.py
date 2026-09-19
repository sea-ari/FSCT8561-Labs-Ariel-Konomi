
#Part3

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
while True:
    data = client_socket.recv(1024)
    if not data:
        break

    message = data.decode()
    print("Client says:", message)

    # Process client commands on the server side
    if message == "Exit":
        reply = "The connection will now close"
        client_socket.send(reply.encode())
        break
    elif message == "is the loop running":
        reply = "Loop is running. This is lab1"
    elif message == "who is this written by":
        reply = "Written by Ariel Konomi"
    else:
        reply = "Server received: " + message

    client_socket.send(reply.encode())

print("Client disconnected from the server...")
client_socket.close()
server_socket.close()

