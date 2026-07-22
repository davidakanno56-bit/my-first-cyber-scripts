import subprocess
import re

def get_saved_wifi_passwords():
    print("=" * 50)
    print("      AKANNO LABS - LOCAL WI-FI KEY RECOVERY")
    print("=" * 50 + "\n")

    try:
        # Step 1: Get raw profile listing
        raw_profiles = subprocess.check_output(
            "netsh wlan show profiles", 
            shell=True, 
            text=True, 
            errors="ignore"
        )
        
        # Step 2: Extract profile names
        profiles = re.findall(r"All User Profile\s*:\s*(.*)", raw_profiles)
        profiles = [p.strip() for p in profiles if p.strip()]

        if not profiles:
            print("[!] No saved Wi-Fi profiles found on this system.")
            return

        # Step 3: Display list in terminal
        print("[*] Saved Wi-Fi Profiles Found:\n")
        for idx, profile in enumerate(profiles, 1):
            print(f"  [{idx}] {profile}")

        choice = input("\nChoose Wi-Fi number to reveal key: ").strip()
        if not choice.isdigit():
            print("[❌] Invalid input. Please enter a number.")
            return

        selected_idx = int(choice) - 1
        if selected_idx < 0 or selected_idx >= len(profiles):
            print("[❌] Selected number out of range.")
            return

        target_wifi = profiles[selected_idx]

        # Step 4: Retrieve cleartext key for selected SSID
        raw_key_info = subprocess.check_output(
            f'netsh wlan show profile "{target_wifi}" key=clear',
            shell=True,
            text=True,
            errors="ignore"
        )

        key_match = re.search(r"Key Content\s*:\s*(.*)", raw_key_info)
        password = key_match.group(1).strip() if key_match else "<OPEN / NO PASSWORD>"

        print("\n" + "=" * 40)
        print(f"  SSID     : {target_wifi}")
        print(f"  PASSWORD : {password}")
        print("=" * 40)

    except Exception as e:
        print(f"[❌] Error: {e}")

if __name__ == "__main__":
    get_saved_wifi_passwords()