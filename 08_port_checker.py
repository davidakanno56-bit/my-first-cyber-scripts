import socket
from datetime import datetime, timezone

# Target configuration (Using local loopback for safe testing)
TARGET_HOST = "127.0.0.1"
PORTS_TO_CHECK = {
    21: "FTP",
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    3389: "RDP"
}

def check_port_status(host, port, service_name):
    """
    Attempts a TCP connection to a specific host and port.
    Returns True if port is reachable, False otherwise.
    """
    # Create a stream socket (IPv4, TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set timeout to 1 second to avoid long hangs
    s.settimeout(1.0)
    
    # connect_ex returns 0 on success (connection established)
    result = s.connect_ex((host, port))
    s.close()
    
    return result == 0

def main():
    print(f"--- NETWORK SERVICE AUDIT FOR: {TARGET_HOST} ---")
    print(f"Time: {datetime.now(timezone.utc).isoformat()}\n")
    
    open_services = []
    
    for port, service in PORTS_TO_CHECK.items():
        is_active = check_port_status(TARGET_HOST, port, service)
        
        if is_active:
            print(f"[✅ ACTIVE] Port {port:<5} | Service: {service}")
            open_services.append((port, service))
        else:
            print(f"[❌ CLOSED] Port {port:<5} | Service: {service}")
            
    print("\n--- SERVICE AUDIT SUMMARY ---")
    print(f"Total Services Checked: {len(PORTS_TO_CHECK)}")
    print(f"Active Responsive Ports: {len(open_services)}")

if __name__ == "__main__":
    main()