import urllib.request
import json
import ipaddress

def enrich_ip_location(ip_address: str) -> dict:
    """
    Enriches a given IPv4/IPv6 address with Geolocation data (Country, City, ISP, Coordinates).
    Uses ip-api.com for free, public endpoint queries.
    """
    # Default fallback object for invalid or internal IPs
    default_data = {
        "ip": ip_address,
        "status": "fail",
        "country": "Internal / Local",
        "city": "Private Network",
        "region": "LAN",
        "isp": "Local Loopback / RFC1918",
        "lat": 0.0,
        "lon": 0.0
    }

    # Step 1: Validate IP address format
    try:
        ip_obj = ipaddress.ip_address(ip_address)
        # Check if the IP is private, loopback, or reserved (e.g., 127.0.0.1, 192.168.x.x, 10.x.x.x)
        if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved:
            return default_data
    except ValueError:
        default_data["country"] = "Invalid IP Format"
        return default_data

    # Step 2: Query public Geolocation API
    url = f"http://ip-api.com/json/{ip_address}?fields=status,country,regionName,city,lat,lon,isp,query"
    
    headers = {
        "User-Agent": "AkannoSOCGeoIP/1.0"
    }

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                if data.get("status") == "success":
                    return {
                        "ip": ip_address,
                        "status": "success",
                        "country": data.get("country", "Unknown"),
                        "region": data.get("regionName", "Unknown"),
                        "city": data.get("city", "Unknown"),
                        "isp": data.get("isp", "Unknown"),
                        "lat": data.get("lat", 0.0),
                        "lon": data.get("lon", 0.0)
                    }
    except Exception as e:
        default_data["country"] = f"Lookup Error ({str(e)})"

    return default_data


# ==========================================
# TEST RUN & DEMONSTRATION
# ==========================================
if __name__ == "__main__":
    print("=" * 60)
    print("      AKANNO LABS - SOC IP GEOLOCATION ENRICHER")
    print("=" * 60 + "\n")

    # Sample public attacker IPs for testing
    sample_ips = [
        "8.8.8.8",         # Google Public DNS (USA)
        "1.1.1.1",         # Cloudflare (Australia / Global)
        "185.220.101.5",   # Sample Public Node (Germany)
        "192.168.1.100"    # Local Private IP
    ]

    for test_ip in sample_ips:
        geo = enrich_ip_location(test_ip)
        print(f"[*] Analyzing IP: {geo['ip']}")
        print(f"    ├─ Country : {geo['country']}")
        print(f"    ├─ City    : {geo['city']}, {geo['region']}")
        print(f"    ├─ ISP     : {geo['isp']}")
        print(f"    └─ Coords  : Lat {geo['lat']} / Lon {geo['lon']}")
        print("-" * 50)