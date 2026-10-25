import ipaddress, socket, nmap, requests
from getpass import getpass


HOST = "127.0.0.1"
PORT = 5274 

client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

#HTTP SCANNER - ariel konomi

def http_scaner():
    
    base_url = input("Enter URL of target: ").strip()
    if not base_url:
        print("A target URL is required.")
        return

   
    headers = ["Content-Security-Policy", "X-Content-Type-Options", "X-Powered-By", "Server"]
    

    try:
        probe_response = requests.get(base_url, timeout=5)

        
        print("Server reported:", probe_response.status_code)

        
        print("Initiating Scan...")

        for header in headers:
            if header in probe_response.headers:
                print("PASS", header, "found")
            else:
                print("ERROR", header, "not found")

        print("Scan completed!")

    
    except requests.RequestException as error:
         print("Error: ", base_url,":", error) 


#PORT SCANNER - ariel konomi

def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((target, port))
    sock.close()
    return result == 0

def run_port_scanner():
    try:

        target = input("Enter target host: ")
        target_ip = socket.gethostbyname(target)


        start_port = int(input("Enter start port: "))
    
        end_port = int(input("Enter end port: "))

    
        if start_port < 1 or end_port > 65535:
            print("Error: Ports must be between 1 and 65535")
        
        elif start_port > end_port:
            print("Error: Start port cannot be greater than end port")
        
        else:
            print("Scanning:", target_ip)
            open_ports = []


        for port in range(start_port, end_port + 1):
            if scan_port(target_ip, port):
            
                try:
                    service = socket.getservbyport(port, "tcp")
                except OSError:
                    service = "unknown"
                
                print ("Port",port,"is OPEN-",service)
                open_ports.append(port)


        print("Scan complete.")

        if len(open_ports) > 0:
            print(len(open_ports),"open ports found")
            print("Open ports:", open_ports)
        else:
            print("No open ports found in the selected range")


    except socket.gaierror:
        print("Error: Invalid hostname or IP address")


    except ValueError:
        print("Error: Please enter valid numbers for the ports")

#USERNAME AND PASSWORD CHECK - ariel konomi

def authentication():
    username = input("Enter your username: ")
    password = getpass("Enter your password: ")

    auth_message = "AUTH|" + username + "|" + password


    client_socket.send(
        auth_message.encode()
    )

    response = client_socket.recv(1024).decode()
    print("Server:", response)

#OTP check - ariel konomi
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
            return True
        else:
            print("Access Denied!")
            return False

    elif response == "ACCESS_DENIED":
        print("Access Denied! Invalid username or password.")
        return False

#MENU BUILD - ariel konomi
try:
    client_socket.connect((HOST, PORT))

    if authentication():        
        while True:
            print()
            print("   OPERATION SENTINEL MENU    ")
            print("Created by: Ariel Konomi - A01375274    ")
            print("   Code based on Labs 0-5")
            print()
            print("Please Choose One of the Following: ")
            print(" [1] Run Port Scanner")
            print(" [2] Run HTTP Checker")
            print(" [3] Request Server PCAP Analysis")
            print(" [EXIT] Disconnect and Quit")
            print()
            print()
            
         
            choice = input("Select an option: ").strip().upper()

            if choice == "1":
                try:
                    run_port_scanner()
                except KeyboardInterrupt:
                    print()
                    print("Port scan interrupted by client. Returning back to the menu selection...")
            elif choice == "2":
                try:
                    http_scaner()
                except KeyboardInterrupt:
                    print()
                    print("HTTP scan interrupted by client. Returning back to the menu selection...")
            elif choice == "3":
                try: 
                    client_socket.send("PCAP|request".encode())
                    pcap_response = client_socket.recv(4096).decode()
                    print()
                    print(pcap_response)
                except KeyboardInterrupt:
                    print()
                    print("PCAP request interrupted by client. Returning back to the menu selection...")
            elif choice == "EXIT":
                client_socket.send("EXIT".encode())
                break
            else:
                print("Invalid choice. Please select 0, 1, 2, or EXIT.")

                print()
except (OSError, EOFError) as error:
    print("Could not connect to the server at", HOST, PORT)
    print("Start the server first:  python server_ariel_konomi_midterm.py")
    client_socket.close()
except KeyboardInterrupt:
    print("Client interrupted via keyboard. Disconnecting...")
    
finally:
    try:
        client_socket.close()
        print("Disconnected successfully... Goodbye")
    except OSError:
        pass
