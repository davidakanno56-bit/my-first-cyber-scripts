import re

# File name to scan
LOG_FILE = "auth_test.log"

# Dictionary to track failed login counts per IP
failed_login_tracker = {}

# Regex pattern for IP addresses
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

print(f"--- SCANNING LOG FILE: {LOG_FILE} ---")

# Open and read the log file line by line
with open(LOG_FILE, "r") as file:
    for line in file:
        # Filter only lines that contain failed logins
        if "Failed password" in line:
            match = re.search(ip_pattern, line)
            if match:
                ip = match.group()
                # Increment count for this IP in our tracker
                failed_login_tracker[ip] = failed_login_tracker.get(ip, 0) + 1

print("\n--- INCIDENT SUMMARY REPORT ---")
# Flag any IP with 3 or more failed attempts as a Brute-Force threat
for ip, count in failed_login_tracker.items():
    if count >= 3:
        print(f"[🚨 BRUTE-FORCE DETECTED] IP: {ip} | Total Failures: {count}")
    else:
        print(f"[⚠️ SUSPICIOUS ATTEMPT] IP: {ip} | Total Failures: {count}")