import re

# 1. Simulated Linux /var/log/auth.log file contents
sample_auth_log = """
Aug 07 16:10:01 server sshd[101]: Accepted password for david from 192.168.1.10 port 45210 ssh2
Aug 07 16:12:15 server sshd[102]: Failed password for root from 192.168.1.50 port 54231 ssh2
Aug 07 16:12:18 server sshd[103]: Failed password for root from 192.168.1.50 port 54232 ssh2
Aug 07 16:12:20 server sshd[104]: Failed password for root from 192.168.1.50 port 54233 ssh2
Aug 07 16:12:23 server sshd[105]: Failed password for admin from 192.168.1.50 port 54234 ssh2
Aug 07 16:12:26 server sshd[106]: Failed password for admin from 192.168.1.50 port 54235 ssh2
Aug 07 16:15:00 server sshd[107]: Failed password for user1 from 10.0.0.8 port 33100 ssh2
"""

print("[-] Processing Linux Authentication Log...")
print("=" * 60)

# Dictionary to track IP address -> failure counts
failed_attempts = {}

# Regular Expression pattern to grab IP addresses from "Failed password" lines
ip_pattern = r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)"

# Split sample log into individual lines and analyze
for line in sample_auth_log.strip().split("\n"):
    match = re.search(ip_pattern, line)
    if match:
        ip_address = match.group(1)
        failed_attempts[ip_address] = failed_attempts.get(ip_address, 0) + 1

# Detection Rule: Flag any IP with 3 or more failed attempts
THRESHOLD = 3

print("\n📊 LOGIN FAILURE SUMMARY BY IP:")
print("-" * 40)
for ip, count in failed_attempts.items():
    print(f"IP: {ip:<15} | Failed Attempts: {count}")
    if count >= THRESHOLD:
        print(f"  🚨 SECURITY ALERT: Potential SSH Brute-Force Attack detected from {ip}!")
        print(f"  🛡️ ACTION: Recommend blocking {ip} at Firewall level.")
print("-" * 40)