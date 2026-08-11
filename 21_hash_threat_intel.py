import hashlib

# 1. Simulated Threat Intelligence Database (Known Malicious SHA-256 Hashes)
THREAT_INTEL_DB = {
    "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": "Trojan.Win32.Generic",
    "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824": "Ransomware.WannaCry.Variant",
    "88d4266fd4e6338d13b845fcf289579d209c897823b9217da3e161936f031589": "Spyware.Keylogger.Agent"
}

def calculate_sha256(data_bytes):
    """Calculates SHA-256 hash of raw bytes."""
    hasher = hashlib.sha256()
    hasher.update(data_bytes)
    return hasher.hexdigest()

print("[-] Threat Intelligence Hash Inspector Online...")
print("=" * 65)

# Test 1: Simulated Clean File
clean_content = b"This is a legitimate company report PDF file."
clean_hash = calculate_sha256(clean_content)

print(f"[+] Inspecting File 1: 'company_report.pdf'")
print(f"    Calculated SHA-256: {clean_hash}")

if clean_hash in THREAT_INTEL_DB:
    print(f"    🚨 MALWARE DETECTED: {THREAT_INTEL_DB[clean_hash]}")
else:
    print("    ✅ CLEAN: Hash not found in threat database.")

print("-" * 65)

# Test 2: Simulated Malicious File (Payload matching WannaCry variant in DB)
malicious_content = b"hello"
malicious_hash = calculate_sha256(malicious_content)

print(f"[+] Inspecting File 2: 'invoice_attachment.exe'")
print(f"    Calculated SHA-256: {malicious_hash}")

if malicious_hash in THREAT_INTEL_DB:
    print(f"    🚨 MALWARE MATCH: {THREAT_INTEL_DB[malicious_hash]}!")
    print("    🛡️ ACTION: Quarantining file and isolating endpoint.")
else:
    print("    ✅ CLEAN: Hash not found in threat database.")

print("=" * 65)