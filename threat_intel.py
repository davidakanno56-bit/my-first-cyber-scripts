import requests

# Target IP flagged from our previous log scanner script
TARGET_IP = "185.220.101.5"

print(f"--- QUERYING THREAT INTELLIGENCE FOR: {TARGET_IP} ---")

# Open security API endpoint (ip-api.com)
url = f"http://ip-api.com/json/{TARGET_IP}"

try:
    # Send HTTP GET Request
    response = requests.get(url, timeout=5)
    
    if response.status_code == 200:
        data = response.json()
        
        if data.get("status") == "success":
            print("\n--- ENRICHED TELEMETRY DATA ---")
            print(f"IP Address:  {data.get('query')}")
            print(f"Country:     {data.get('country')}")
            print(f"City:        {data.get('city')}")
            print(f"ISP / Org:   {data.get('isp')}")
            print(f"AS Name:     {data.get('as')}")
            
            # Security logic to flag Tor exit nodes or hosting providers
            org_info = str(data.get('isp')).lower() + " " + str(data.get('as')).lower()
            if "tor" in org_info or "hosting" in org_info or "servers" in org_info:
                print("\n🚨 THREAT SCORE: HIGH RISK (Known Proxy / Tor / Hosting Provider)")
            else:
                print("\n⚠️ THREAT SCORE: MEDIUM RISK (External Host)")
        else:
            print(f"\n❌ API Query Error: {data.get('message')}")
            
    else:
        print(f"\n❌ HTTP Error. Status Code: {response.status_code}")

except Exception as e:
    print(f"\n❌ Network Error: {e}")