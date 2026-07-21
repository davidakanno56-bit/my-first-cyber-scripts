# ==========================================
# MODULE 1: STRING PARSING & IP ISOLATION
# Goal: Extract clean IP addresses from raw log entries
# ==========================================

# 1. RAW LOG ENTRY (Standard Syslog format)
raw_log = "2026-07-21 14:22:01 [SECURITY_ALERT] Failed login attempt from 103.21.244.0 on port 22"

print("--- RAW LOG STRING ---")
print(raw_log)

# 2. STRING SPLITTING: Break the log into individual words/tokens
# .split(" ") turns the sentence into a List of words separated by spaces
log_words = raw_log.split(" ")

print("\n--- SPLIT INTO LIST OF WORDS ---")
print(log_words)

# 3. EXTRACTING THE TARGET IP
# In this specific log structure, the IP address is at index position 7
target_ip = log_words[7]

print("\n--- EXTRACTED DATA ---")
print(f"Detected Suspicious IP: {target_ip}")

# 4. STRING CLEANING & SANITIZATION
# Check if the IP starts with a standard local range
if target_ip.startswith("192.168."):
    print(f"Network Scope: INTERNAL NETWORK ({target_ip})")
else:
    print(f"Network Scope: EXTERNAL / PUBLIC ({target_ip})")
    