import urllib.parse
import re

LOG_FILE = "web_access.log"

# Define attack signature patterns
ATTACK_PATTERNS = {
    "SQL_INJECTION": r"(\'|\"|%27|%22)\s*(OR|AND|UNION|SELECT)",
    "XSS_ATTACK": r"(<script>|%3Cscript%3E)",
    "PATH_TRAVERSAL": r"(\.\./|\.\.\\|/etc/passwd)"
}

def analyze_web_logs(file_path):
    print(f"--- SCANNING WEB ACCESS LOG: {file_path} ---")
    
    with open(file_path, "r") as file:
        for line_num, line in enumerate(file, 1):
            # Decode URL-encoded characters (e.g., %20 -> space, %27 -> ')
            decoded_line = urllib.parse.unquote(line)
            
            # Check line against defined security patterns
            for attack_type, pattern in ATTACK_PATTERNS.items():
                if re.search(pattern, decoded_line, re.IGNORECASE):
                    # Extract IP (first element in Nginx/Apache logs)
                    ip = line.split()[0]
                    print(f"\n[🚨 {attack_type} DETECTED]")
                    print(f" Line: {line_num} | Attacker IP: {ip}")
                    print(f" Request: {decoded_line.strip()}")

if __name__ == "__main__":
    analyze_web_logs(LOG_FILE)