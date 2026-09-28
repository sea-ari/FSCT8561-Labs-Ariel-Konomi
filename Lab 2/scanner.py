import socket

port = 80

def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((target, port))
    sock.close()
    return result == 0 

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