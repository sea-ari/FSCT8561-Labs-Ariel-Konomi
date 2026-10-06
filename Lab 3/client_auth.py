import socket
from getpass import getpass

HOST = "127.0.0.1"
PORT = 12345

client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client_socket.connect((HOST, PORT))

username = input("Username: ")
password = getpass("Password: ")

auth_message = "AUTH|" + username + "|" + password

client_socket.send(
    auth_message.encode()
)

response = client_socket.recv(1024).decode()
print("Server:", response)

if response == "OTP_REQUIRED":

    otp_code = input("Enter your 6-digit OTP: ")

    otp_message = "OTP|" + otp_code

    client_socket.send(
        otp_message.encode()
    )

    final_response = client_socket.recv(1024).decode()

    print("Server:", final_response)

    if final_response == "ACCESS_GRANTED":
        print("Access Granted! Login successful.")
    else:
        print("Access Denied!")

elif response == "ACCESS_DENIED":
    print("Access Denied! Invalid username or password.")

client_socket.close()
print("Disconnected")