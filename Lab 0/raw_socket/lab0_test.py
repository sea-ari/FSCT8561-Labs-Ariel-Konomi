
print("My first Python security program")
print()

#Part 1
print("PART1")
course = "FSCT 8561 Ariel Konomi"
port = 12345
print(course)
print(port)
print()

#Library
import socket
print("Socket library loaded successfully")
print()

#Tuples
address = ("127.0.0.1", 12345, "Ariel Konomi")
print(address)
print()

#Strings and bytes
message = "Hello Ariel Konomi"
data = message.encode()
print(message)
print(data)
print(data.decode())
print()
print("PART2")

#Understanding sockets
import socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("TCP socket created successfully")
my_socket.close()
print()
print("PART3")

socket() → bind() → listen() → accept() → recv() → send() → close()

