import urllib.request

# Define the target web server
url = "http://example.com"

print("[-] Sending HTTP Request to target server...")

# This line opens a network socket and triggers the 3-Way Handshake (SYN -> SYN-ACK -> ACK)
response = urllib.request.urlopen(url)

# Read response headers (The server's answer)
status_code = response.getcode()
server_header = response.headers.get('Server')

print(f"[+] Handshake & Request Successful!")
print(f"[+] Status Code: {status_code} (200 means OK)")
print(f"[+] Remote Server Type: {server_header}")