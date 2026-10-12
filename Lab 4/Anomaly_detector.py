from scapy.all import rdpcap, IP, TCP, UDP

packets = rdpcap("botnet-capture-20110812-rbot.pcap")

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
print("Total TCP packets:", tcp_count)
print("Total UDP packets:", udp_count)
print("List of suspicious IPs:", len(alerted_ips))