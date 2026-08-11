import re
from collections import Counter
import json
import urllib.request

# 1. Sample Log Data (Includes public IPs so GeoIP lookup returns real locations)
sample_logs = """
Jul 29 14:02:11 server sshd[1234]: Failed password for invalid user admin from 185.220.101.5 port 54321 ssh2
Jul 29 14:02:15 server sshd[1234]: Failed password for root from 185.220.101.5 port 54322 ssh2
Jul 29 14:02:18 server sshd[1234]: Failed password for root from 185.220.101.5 port 54323 ssh2
Jul 29 14:02:22 server sshd[1234]: Failed password for user david from 185.220.101.5 port 54324 ssh2
Jul 29 14:02:25 server sshd[1234]: Failed password for user david from 185.220.101.5 port 54325 ssh2
Jul 29 14:02:30 server sshd[1234]: Failed password for root from 198.51.100.42 port 43210 ssh2
Jul 29 14:03:01 server sshd[1234]: Accepted password for david from 10.0.0.15 port 33112 ssh2
"""

# Threshold for triggering a Brute-Force Alert
FAILURE_THRESHOLD = 3

def parse_failed_logins(log_data):
    """Parses raw logs using Regular Expressions to extract IPs with failed attempts."""
    ip_pattern = r"Failed password.*from\s+([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})"
    failed_ips = re.findall(ip_pattern, log_data)
    return Counter(failed_ips)

def detect_threats(ip_counts, threshold):
    """Flags IPs exceeding the failure threshold."""
    flagged_threats = {}
    for ip, count in ip_counts.items():
        if count >= threshold:
            flagged_threats[ip] = {
                "failed_attempts": count,
                "status": "ALERT_BRUTE_FORCE_DETECTED"
            }
    return flagged_threats

def get_ip_geolocation(ip_address):
    """Fetches public geolocation intelligence for a flagged IP."""
    url = f"http://ip-api.com/json/{ip_address}"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            if data.get("status") == "success":
                return {
                    "country": data.get("country"),
                    "isp": data.get("isp"),
                    "org": data.get("org")
                }
    except Exception as e:
        return {"error": f"Failed to fetch GeoIP: {str(e)}"}
    
    return {"country": "Unknown/Private IP", "isp": "Internal Network"}

if __name__ == "__main__":
    print("Parsing logs for suspicious activity...")
    counts = parse_failed_logins(sample_logs)
    threats = detect_threats(counts, FAILURE_THRESHOLD)
    
    # Enrich flagged IPs with Geolocation intelligence
    for ip in threats:
        print(f"Enriching threat intelligence for {ip}...")
        threats[ip]["geo_intel"] = get_ip_geolocation(ip)
    
    print("\n--- ENRICHED THREAT REPORT ---")
    print(json.dumps(threats, indent=4))