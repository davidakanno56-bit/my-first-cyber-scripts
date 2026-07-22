from scapy.all import sniff, IP, TCP, UDP, ICMP
from datetime import datetime, timezone

def packet_callback(packet):
    """Callback function triggered for every intercepted network packet."""
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        ttl = packet[IP].ttl
        proto_num = packet[IP].proto

        # Map protocol number to string label
        protocol_map = {6: "TCP", 17: "UDP", 1: "ICMP"}
        proto_name = protocol_map.get(proto_num, f"Proto-{proto_num}")

        timestamp = datetime.now(timezone.utc).strftime("%H:%M:%S")

        # Extract source and destination ports if available
        src_port = ""
        dst_port = ""
        if packet.haslayer(TCP):
            src_port = f":{packet[TCP].sport}"
            dst_port = f":{packet[TCP].dport}"
        elif packet.haslayer(UDP):
            src_port = f":{packet[UDP].sport}"
            dst_port = f":{packet[UDP].dport}"

        print(f"[{timestamp}] [{proto_name:<4}] {src_ip}{src_port} -> {dst_ip}{dst_port} | TTL: {ttl}")

def start_sniffer(packet_count=10):
    print("=" * 60)
    print("      AKANNO LABS - LAYER 3/4 LIVE PACKET SNIFFER")
    print("=" * 60)
    print(f"[*] Capturing {packet_count} packets on default interface...\n")

    # Capture packets using Scapy
    sniff(prn=packet_callback, count=packet_count, store=False)
    
    print("\n[✅] Packet capture session complete.")

if __name__ == "__main__":
    start_sniffer(packet_count=10)