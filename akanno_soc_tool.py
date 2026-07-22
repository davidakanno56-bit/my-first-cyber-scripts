import re
import json
import urllib.parse
import requests
from datetime import datetime, timezone

# --- CONFIGURATION & ATTACK SIGNATURES ---
AUTH_LOG = "auth_test.log"
WEB_LOG = "web_access.log"
IP_PATTERN = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

WEB_ATTACK_PATTERNS = {
    "SQL_INJECTION": r"(\'|\"|%27|%22)\s*(OR|AND|UNION|SELECT)",
    "XSS_ATTACK": r"(<script>|%3Cscript%3E)",
    "PATH_TRAVERSAL": r"(\.\./|\.\.\\|/etc/passwd)"
}

class SOCTelemetryEngine:
    def __init__(self):
        self.events = []
        self.failed_auth_counts = {}

    def process_auth_logs(self, file_path):
        """Scans authentication logs for brute-force patterns."""
        print(f"[*] Ingesting Auth Log: {file_path}")
        try:
            with open(file_path, "r") as f:
                for line in f:
                    if "Failed password" in line:
                        match = re.search(IP_PATTERN, line)
                        if match:
                            ip = match.group()
                            self.failed_auth_counts[ip] = self.failed_auth_counts.get(ip, 0) + 1
            
            # Record alerts based on threshold
            for ip, count in self.failed_auth_counts.items():
                severity = "CRITICAL" if count >= 3 else "MEDIUM"
                self.events.append({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "category": "AUTHENTICATION",
                    "event_type": "BRUTE_FORCE_ATTEMPT" if count >= 3 else "FAILED_LOGIN",
                    "source_ip": ip,
                    "failure_count": count,
                    "severity": severity
                })
        except FileNotFoundError:
            print(f"[!] File not found: {file_path}")

    def process_web_logs(self, file_path):
        """Scans web logs for URL payload signatures."""
        print(f"[*] Ingesting Web Log: {file_path}")
        try:
            with open(file_path, "r") as f:
                for line in f:
                    decoded = urllib.parse.unquote(line)
                    for attack_type, pattern in WEB_ATTACK_PATTERNS.items():
                        if re.search(pattern, decoded, re.IGNORECASE):
                            ip = line.split()[0]
                            self.events.append({
                                "timestamp": datetime.now(timezone.utc).isoformat(),
                                "category": "WEB_APPLICATION",
                                "event_type": attack_type,
                                "source_ip": ip,
                                "raw_request": decoded.strip(),
                                "severity": "HIGH"
                            })
        except FileNotFoundError:
            print(f"[!] File not found: {file_path}")

    def export_json(self, output_file="final_telemetry.json"):
        """Serializes captured telemetry into formatted JSON."""
        with open(output_file, "w") as f:
            json.dump(self.events, f, indent=4)
        print(f"\n[✅] Telemetry export complete: '{output_file}' ({len(self.events)} events recorded)")

def main():
    print("=" * 50)
    print("      AKANNO LABS - SOC TELEMETRY ENGINE v1.0")
    print("=" * 50 + "\n")
    
    engine = SOCTelemetryEngine()
    engine.process_auth_logs(AUTH_LOG)
    engine.process_web_logs(WEB_LOG)
    engine.export_json()

if __name__ == "__main__":
    main()