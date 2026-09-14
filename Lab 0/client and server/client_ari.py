#Part8
import socket

HOST = "127.0.0.1"
PORT = 80

client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client_socket.connect((HOST, PORT))

message = "Hello Server. This is for Part 8 of Lab0 - Ariel Konomi"

client_socket.send(message.encode())

response = client_socket.recv(1024)

print(response.decode())

client_socket.close()