

client_socket.connect((HOST, PORT))

`client_socket.connect()`:  connects to the server's ip address and port



def receive_messages():
    while True:
        try:

`def receive_messages():`: defines the blueprint for your background listening task
`while True:`: an infinite loop so it constantly waits for new messages until it is broken
`try:`: starts an error-handling block so the client doesn't crash if the server turns off abruptly



response = client_socket.recv(1024)
    if not response:
        break

`response = client_socket.recv(1024)`: waits to receive up to 1024 bytes from the server
`if not response:`
`break`: exit the infinite loop as the server has probably disconnected




print("\n" + response.decode())
except:
    break

`print()`: converts the network bytes back to text and prints them 
`except: break`: if any networking error happens, break the loop




username = input("Enter your username: ")
hello_message = "HELLO|" + username
client_socket.send(hello_message.encode())

`username = input()`: asks user to type name into the terminal
`hello_message = `:  the required protocol command (HELLO|) to the front of the name
`client_socket.send()`: converts the string into bytes (.encode()) and sends it to the server




response = client_socket.recv(1024)
print("Server:", response.decode())

`response = recv(1024)`: waits for the server's single "OK|Hello" confirmation




listener = threading.Thread(target=receive_messages)
listener.daemon = True 
listener.start()

`threading.Thread(target=receive_messages)`: creates a background thread and assigns it the receive_messages function written earlier
`listener.daemon = True`: marks this thread as a "daemon". if i close my main program, force this background thread to die too
`listener.start()`: turns the background worker on and lets it listen for commands




while True:
    message = input("Enter message or type EXIT to leave: ")

`message = input()`: waits for input



if message.upper() == "EXIT":
    client_socket.send("EXIT|".encode())
    break

`if message.upper() == "EXIT":`: Checks if you typed "EXIT" 
`send("EXIT|")`: sends the official protocol exit command to the server





protocol_message = "MSG|" + message
client_socket.send(protocol_message.encode())

`protocol_message = "MSG|" + message`: assumes a chat message was sent




client_socket.close()
print("Disconnected")

`client_socket.close()`: once the while loop breaks, severs the TCP connection to the server
