import json
import subprocess
import os

TELEMETRY_FILE = "final_telemetry.json"

def block_ip_windows_firewall(ip_address):
    """
    Executes netsh advfirewall to add a inbound BLOCK rule for a given IP address.
    Requires Administrator privileges.
    """
    rule_name = f"Akanno_Labs_Block_{ip_address}"
    cmd = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block remoteip={ip_address}'
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[✅ FIREWALL RULE APPLIED] Successfully blocked inbound traffic from IP: {ip_address}")
        else:
            print(f"[⚠️ WARNING] Failed to block {ip_address}. Ensure terminal is run as Administrator.")
            print(f"    Details: {result.stderr.strip()}")
    except Exception as e:
        print(f"[❌ ERROR] Exception occurred while executing firewall command: {e}")

def process_active_defense():
    print("=" * 50)
    print("      AKANNO LABS - SOAR AUTOMATED DEFENSE ENGINE")
    print("=" * 50 + "\n")

    if not os.path.exists(TELEMETRY_FILE):
        print(f"[!] Telemetry file '{TELEMETRY_FILE}' not found. Run 'akanno_soc_tool.py' first.")
        return

    with open(TELEMETRY_FILE, "r") as f:
        events = json.load(f)

    blocked_ips = set()

    for event in events:
        # Trigger firewall block on High/Critical severity events
        severity = event.get("severity", "").upper()
        ip = event.get("source_ip")

        if severity in ["CRITICAL", "HIGH"] and ip:
            if ip not in blocked_ips:
                print(f"[🚨 HIGH RISK DETECTED] Event: {event.get('event_type')} | IP: {ip}")
                block_ip_windows_firewall(ip)
                blocked_ips.add(ip)

    print(f"\n[ SUMMARY] Total Unique IPs Blocked: {len(blocked_ips)}")

if __name__ == "__main__":
    process_active_defense() 