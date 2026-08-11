import socket

domain = "example.com"

print(f"[-] Asking DNS server for the IP address of '{domain}'...")

# socket.gethostbyname resolves the domain to an IP address via DNS
ip_address = socket.gethostbyname(domain)

print(f"[+] DNS Lookup Complete!")
print(f"[+] Domain : {domain}")
print(f"[+] IP     : {ip_address}")