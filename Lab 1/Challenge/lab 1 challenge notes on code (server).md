

import socket
import threading

`import socket`: brings in Python’s built-in networking library to create raw TCP connections
`import threading`: brings in the library that allows doing multiple things at once 



HOST = "127.0.0.1"
PORT = 12345

`HOST`: sets the server to listen on the localhost
`PORT`: chooses port 12345 for the network traffic to travel through



server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

`server_socket` = : creates the main factory socket. 
`AF_INET` means it uses IPv4 addresses, and `SOCK_STREAM` means it uses the TCP protocol



server_socket.bind((HOST, PORT))
server_socket.listen(5)
print("Server is waiting for connection(s)...")

`bind()`: claims the IP and Port so no other program on the computer can use them
`listen(5)`: turns the socket on to listen for incoming connections. it will allow up to 5 people to wait in line



clients = {}

`clients = {}`: Creates an empty dictionary to remember the socket and username of every person who connects




def handle_client(client_socket):
    username = None
    connected = True

`def handle_client()`: defines the function. It takes `client_socket` as an argument so it knows who it is talking to
`username = None`: starts the user off without a name
`connected = True`: switch to keep the upcoming `while` loop running




while connected:
    try:

`while connected:`: starts an infinite loop to keep the conversation going
`try:`: starts an error-handling block so the client doesn't crash if the server turns off abruptly




data = client_socket.recv(1024)
    if not data:
        print("Client disconnected unexpectedly")
        break

`data = recv(1024)`: waits to receive up to 1024 bytes from the user
`if not data:`: 
`break`:exit the infinite loop as the client has probably disconnected



message = data.decode()

`message = data.decode()`:  converts the network bytes back to text




if "|" not in message:
    client_socket.send("ERROR|Invalid command format".encode())
    continue

`if "|" not in message:`: checks to make sure the client followed the rules of the protocol set
`send(...encode())`: if it wasn't followed, sends an error message back
`continue`: skips the rest of the code below and forces the `while` loop to start over at `recv()`




command, content = message.split("|", 1)

`.split("|", 1)`: divides the string into two pieces. The left side is the `command`, and the right side is the `content`






if command == "HELLO":
    if content == "":
        client_socket.send("ERROR|Username required".encode())

`if command == "HELLO":`: checks if the user is trying to log in
`if content == "":`: checks if they sent an empty name and sends an error if they did





else:
    username = content
    clients[client_socket] = username
    print(f"User connected: {username}")
    client_socket.send(("OK|Hello " + username).encode())

`username = content`: remembers the user's name in the specific thread
`clients[client_socket] = username`: adds the user's socket and name to the global dictionary so the other threads know the user exists
`send`: sends a welcome message back to the user





elif command == "MSG":
    if username is None:
	    client_socket.send("ERROR|HELLO required first".encode())
	elif content == "":
	    client_socket.send("ERROR|Message cannot be empty".encode())
    elif len(content) > 200:
        client_socket.send("ERROR|Message too long".encode())

`elif command == "MSG":`: checks if they are sending a chat message
`if username is None:`: blocks the message if they haven't sent `HELLO` yet
`elif content == "":`: blocks empty messages
`elif len(content) > 200:`: blocks messages over 200 characters




else:
    broadcast_msg = f"{username} says: {content}"
                    
    for other_socket in clients:
        if other_socket != client_socket:
            other_socket.send(broadcast_msg.encode())
                            
    client_socket.send("OK|Message sent".encode())

`broadcast_msg = `: formats the string to show who is speaking
`for other_socket in clients:`: loops through every single user saved in the global `clients` dictionary
`if other_socket != client_socket:`: makes sure it doesn't send the message back to the person who just typed it
`other_socket.send()`: sends the message to the other users
`client_socket.send()`: sends a private message sent confirmation to the client who wrote the message





elif command == "EXIT":
    client_socket.send("OK|Goodbye".encode())
    connected = False
else:
    client_socket.send("ERROR|Unknown command".encode())

`elif command == "EXIT":`: checks if the user wants to leave
`send()`: sends a goodbye message
`connected = False`: changes the switch to False, which breaks the while loop
`else:`: catches any commands that aren't HELLO, MSG, or EXIT




except ConnectionResetError:
    print("Connection reset by client")
    break

`except ConnectionResetError:`: if the client forces their terminal to close, closes the connection






client_socket.close()
print("A client disconnected")

`client_socket.close()`: closes the TCP connection





while True:
    client_socket, client_address = server_socket.accept()

`while True:`: keeps the server running
` = server_socket.accept()`: when a new user connects, this line wakes up and creates a dedicated `client_socket`




client_thread = threading.Thread(target=handle_client, args=(client_socket,))
client_thread.start()

`threading.Thread()`: creates a background thread. It tells the worker to run the `handle_client` function, and passes the new `client_socket`
`client_thread.start()`: the background worker takes over talking to the user, and the main 