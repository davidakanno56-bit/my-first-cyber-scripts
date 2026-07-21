import re  # 're' is Python's built-in Regular Expression library

# 1. MESSY, UNSTRUCTURED LOG (IP is at a different position!)
raw_log = "USER_AUTH_FAIL: High severity alert from host server. Malicious origin IP 103.21.244.0 targeted admin profile."

print("--- RAW LOG STRING ---")
print(raw_log)

# 2. REGEX PATTERN FOR IP ADDRESSES
# \d{1,3} matches 1 to 3 digits. The \. matches a literal dot.
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

# 3. SEARCH THE LOG USING REGEX
match = re.search(ip_pattern, raw_log)

if match:
    extracted_ip = match.group()
    print("\n--- REGEX MATCH FOUND ---")
    print(f"Extracted IP Address: {extracted_ip}")
    
    # Check if it's a suspicious public IP
    if not extracted_ip.startswith("192.168.") and not extracted_ip.startswith("10."):
        print("🚨 ACTION REQUIRED: Send telemetry alert to Elastic Cloud SIEM!")
else:
    print("\nNo IP address found in log.")