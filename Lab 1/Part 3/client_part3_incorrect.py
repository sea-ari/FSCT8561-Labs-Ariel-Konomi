#Part3
import socket

HOST = "127.0.0.1"
PORT = 80

client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client_socket.connect((HOST, PORT))

message = "Hello Server. This is for Part 3 of Lab1 - Ariel Konomi"

client_socket.send(message.encode())

response = client_socket.recv(1024)

print(response.decode())

print()
print()


print()
print()


while True:
    command = input("Please write a message: ")

    if command == "is the loop running":
        print("Loop is running. This is lab1")
    elif command == "who is this written by":
        print("Written by Ariel Konomi")    
    elif command == "Exit":
        print("The connection will now close")
        break


client_socket.close()