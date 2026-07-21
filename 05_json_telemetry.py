import re
import json
from datetime import datetime, timezone

# 1. REUSABLE FUNCTION TO PARSE LOGS
def parse_security_log(log_line):
    """
    Parses a single log string and returns a structured dictionary if a threat is detected.
    """
    ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    
    # Check for authentication failures
    if "Failed password" in log_line or "USER_AUTH_FAIL" in log_line:
        match = re.search(ip_pattern, log_line)
        if match:
            extracted_ip = match.group()
            
            # Build a structured security event (Dictionary)
            telemetry_event = {
               "timestamp": datetime.now(timezone.utc).isoformat(),
                "event_type": "AUTHENTICATION_FAILURE",
                "source_ip": extracted_ip,
                "severity": "HIGH" if not extracted_ip.startswith("192.168.") else "LOW",
                "raw_message": log_line.strip()
            }
            return telemetry_event
            
    return None


# 2. MAIN EXECUTION WORKFLOW
def main():
    print("--- STARTING TELEMETRY PARSER ENGINE ---")
    
    sample_logs = [
        "2026-07-21 10:00:01 Accepted password for david from 192.168.1.50 port 22",
        "2026-07-21 10:05:12 Failed password for root from 185.220.101.5 port 22",
        "2026-07-21 10:20:44 USER_AUTH_FAIL: High severity alert from 45.33.32.156"
    ]
    
    alerts_payload = []
    
    for log in sample_logs:
        event = parse_security_log(log)
        if event:
            alerts_payload.append(event)
            
    # Convert Python List/Dict into formatted JSON String (SIEM-ready)
    json_output = json.dumps(alerts_payload, indent=4)
    
    print("\n--- GENERATED SIEM TELEMETRY (JSON) ---")
    print(json_output)
    
    # Save directly to a JSON file on disk
    with open("siem_telemetry.json", "w") as json_file:
        json_file.write(json_output)
        print("\n✅ Telemetry successfully exported to 'siem_telemetry.json'")

if __name__ == "__main__":
    main()