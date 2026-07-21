from datetime import datetime, timezone

# 1. DEFINE THE CLASS (Blueprint for a Security Alert)
class SecurityAlert:
    def __init__(self, source_ip, attack_type, severity="MEDIUM"):
        self.source_ip = source_ip
        self.attack_type = attack_type
        self.severity = severity
        self.timestamp = datetime.now(timezone.utc).isoformat()
        self.status = "OPEN"  # Default state when alert is generated

    # Method to escalate alert severity
    def escalate(self, new_severity="HIGH"):
        self.severity = new_severity
        print(f"🚨 ALERT ESCALATED for {self.source_ip} -> New Severity: {self.severity}")

    # Method to display formatted alert details
    def display_alert(self):
        print(f"[{self.timestamp}] [{self.status}] {self.severity} - {self.attack_type} from {self.source_ip}")


# 2. MAIN WORKFLOW
def main():
    print("--- INSTANTIATING SECURITY ALERTS ---")
    
    # Create two distinct alert objects using the class blueprint
    alert1 = SecurityAlert("185.220.101.5", "SSH Brute-Force")
    alert2 = SecurityAlert("192.168.1.10", "Port Scan", severity="LOW")

    # Display initial state
    alert1.display_alert()
    alert2.display_alert()

    # Escalate alert1 based on threat logic
    print("\n--- TRIGGERING AUTOMATED SOC PLAYBOOK ---")
    alert1.escalate("CRITICAL")
    
    # Display updated state
    alert1.display_alert()

if __name__ == "__main__":
    main()