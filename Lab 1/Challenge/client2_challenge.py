import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client_socket.connect((HOST, PORT))

def receive_messages():
    while True:
        try:
            response = client_socket.recv(1024)
            if not response:
                break
            
            # Print the message from the server/other users
            print("\n" + response.decode())
        except:
            break

username = input("Enter your username: ")

hello_message = "HELLO|" + username

client_socket.send(
    hello_message.encode()
)

response = client_socket.recv(1024)

print("Server:", response.decode())


listener = threading.Thread(target=receive_messages)
listener.daemon = True 
listener.start()

while True:
    message = input(
        "Enter message or type EXIT to leave: "
    )

    if message.upper() == "EXIT":

        client_socket.send(
            "EXIT|".encode()
        )
        break

    protocol_message = "MSG|" + message

    client_socket.send(
        protocol_message.encode()
    )

client_socket.close()

print("Disconnected")