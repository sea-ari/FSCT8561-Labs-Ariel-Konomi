import socket, hashlib, pyotp, logging, time
from scapy.all import  rdpcap, IP, TCP, UDP, ICMP

HOST = "127.0.0.1"
PORT = 5274 

MAX_AUTH_FAILURES = 3
MAX_OTP_FAILURES = 3

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, stored_hash):
    return hash_password(password) == stored_hash

def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret)
    
    return totp.verify(otp.strip(), valid_window=1)


ariel_secret = "PBGRS77FESD2GRGH"

users = {
    "ariel": {
        "password_hash": hash_password("Midterm123!"),
        "totp_secret": ariel_secret
    }
}

#PCAP ANALYSIS - ariel konomi

def run_pcap_analysis():
    
    packets = rdpcap("FSCT8561_Operation_Sentinel_Traffic.pcap")
    try:
        tcp_count = 0
        udp_count = 0
        ip_timestamps = {}
        alerted_ips = []

        for pkt in packets:
            if IP in pkt:
        
                if TCP in pkt or UDP in pkt:
                    if TCP in pkt:
                        tcp_count = tcp_count + 1
                    elif UDP in pkt:
                        udp_count = udp_count + 1
                    else: 
                        continue

                    src_ip = pkt[IP].src
                    current_time = float(pkt.time)

                    if src_ip not in ip_timestamps:
                        ip_timestamps[src_ip] = []

                    ip_timestamps[src_ip].append(current_time)

                    valid_timestamps = []
                    for old_time in ip_timestamps[src_ip]:
                        if current_time - old_time <= 5.0:
                            valid_timestamps.append(old_time)
                    ip_timestamps[src_ip] = valid_timestamps

                    if len(ip_timestamps[src_ip]) > 20:
                        if src_ip not in alerted_ips:
                            alerted_ips.append(src_ip)
                            print("WARNING: OVER 20 packets from IP:", src_ip, "in 5 seconds!!")
        print()
        print("File analyzed:", packets)
        print("Total TCP packets:", tcp_count)
        print("Total UDP packets:", udp_count)
        print("List of suspicious IPs:", len(alerted_ips))
        print()
        packets_summary = (
                "File analyzed:" + str(packets) + "\n"+
                "Total TCP packets:" + str(tcp_count) + "\n"+
                "Total UDP packets:" + str(udp_count) + "\n"+
                "List of suspicious IPs (over 20 packets in 5 seconds):"+ str(len(alerted_ips))
        )
        return packets_summary
    except FileNotFoundError:
        return "ERROR|PCAP file not found on server"
    except Exception as err:
        return f"ERROR|PCAP analysis failed: {str(err)}"

#AUTHENTICATION - ariel konomi

def authentication():

    server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
    )
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print("Server is waiting for a connection...")
    totp = pyotp.TOTP(ariel_secret)
    seconds_remaining = 30 - (int(time.time()) % 30)
    print(f"{totp.now()} ({seconds_remaining}s left in current window)")
    
    client_socket, client_address = server_socket.accept()
    print("Connected by:", client_address)

    password_verified = False
    authenticated_user = None
    
    try:
        while True:    

            data = client_socket.recv(1024)

            if not data:
                print("Client disconnected unexpectedly")
                break

            message = data.decode()
            print("Received:", message)

            if "|" not in message:
                client_socket.send(
                    "ERROR|Invalid command format".encode()
                )
                continue

            parts = message.split("|")
            command = parts[0]

            if command == "AUTH":

                if len(parts) != 3:
                    client_socket.send(
                        "ERROR|Malformed AUTH message".encode()
                    )
                    continue

                username = parts[1]
                password = parts[2]

                if username in users and verify_password(password, users[username]["password_hash"]):
                    password_verified = True
                    authenticated_user = username
                
                
                    current_code = pyotp.TOTP(users[username]["totp_secret"]).now()
                    time_left = 30 - (int(time.time()) % 30)
                    print(f"Password verified for: {username}")
                    print(f"Valid OTP to enter: {current_code} ({time_left}s remaining)")

                    client_socket.send(
                        "OTP_REQUIRED".encode()
                    )
                else:
                    password_verified = False
                    authenticated_user = None
                    print("Auth failed for:", username)

                    client_socket.send(
                        "ACCESS_DENIED".encode()
                    )

            elif command == "OTP":

                if len(parts) != 2:
                    client_socket.send(
                        "ERROR|Malformed OTP message".encode()
                    )
                    continue

                otp_code = parts[1]

                if not password_verified or authenticated_user is None:
                    print("OTP rejected: Password not verified first")
                    client_socket.send(
                        "ACCESS_DENIED".encode()
                    )
                else:
                    secret = users[authenticated_user]["totp_secret"]

                    if verify_otp(secret, otp_code):
                        print("Authentication successful for:", authenticated_user)
                        client_socket.send(
                            "ACCESS_GRANTED".encode()
                        )
                        break
                    else:
                        print("Invalid OTP for:", authenticated_user)
                        client_socket.send(
                            "ACCESS_DENIED".encode()
                        )
                        break
            else:
                client_socket.send(
                    "ERROR|Unknown command".encode()
                )
   
        while True:
            request_data = client_socket.recv(1024)
            if not request_data:
                break

            request = request_data.decode().strip()

            if request == "PCAP|request":
                print("PCAP analysis has been requested by client...")
                pcap_result = run_pcap_analysis()
                client_socket.sendall(pcap_result.encode())
            elif request == "EXIT":
                print("Client requested to disconnect")
                break
            else:
                client_socket.sendall("ERROR|Unknown command request".encode())

    except (OSError, ConnectionResetError) as error:
        print("Server error:", error)
    finally:
        client_socket.close()
        server_socket.close()
        print("Server closed")

if __name__ == "__main__":
    authentication()