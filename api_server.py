import json
import os
import subprocess
import re
import importlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from akanno_soc_tool import SOCTelemetryEngine, AUTH_LOG, WEB_LOG
from geoip_enricher import enrich_ip_location

# Safely import 04_threat_intel dynamically using importlib
try:
    threat_module = importlib.import_module("04_threat_intel")
    # Dynamically find whichever function name you used in 04_threat_intel.py
    query_threat_intel = (
        getattr(threat_module, "enrich_ip", None) or 
        getattr(threat_module, "query_abuseipdb_free", None) or 
        getattr(threat_module, "query_threat_intel", None)
    )
except ModuleNotFoundError:
    # Fallback if the file was renamed to threat_intel.py
    from threat_intel import query_threat_intel

app = FastAPI(title="Akanno Labs SOC API", version="5.0")

# Enable CORS for frontend clients (Bolt.new / React)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TELEMETRY_FILE = "final_telemetry.json"


# --- HELPER FUNCTIONS ---

def refresh_telemetry():
    """Runs the engine to process logs and refresh final_telemetry.json."""
    engine = SOCTelemetryEngine()
    engine.process_auth_logs(AUTH_LOG)
    engine.process_web_logs(WEB_LOG)
    engine.export_json(TELEMETRY_FILE)


def fetch_wifi_data():
    """Fetches saved Wi-Fi profiles and keys from the local system."""
    wifi_list = []
    try:
        output = subprocess.check_output(
            "netsh wlan show profiles", shell=True, stderr=subprocess.DEVNULL
        ).decode('utf-8', errors='ignore')
        
        profiles = [p.strip() for p in re.findall(r"All User Profile\s*:\s*(.*)", output)]
        
        for ssid in profiles:
            try:
                cmd = f'netsh wlan show profile name="{ssid}" key=clear'
                pass_output = subprocess.check_output(
                    cmd, shell=True, stderr=subprocess.DEVNULL
                ).decode('utf-8', errors='ignore')
                
                key_match = re.search(r"Key Content\s*:\s*(.*)", pass_output)
                password = key_match.group(1).strip() if key_match else "[Open / Protected]"
            except Exception:
                password = "[Unavailable]"
                
            wifi_list.append({"ssid": ssid, "password": password})
    except Exception as e:
        print(f"Error fetching Wi-Fi profiles: {e}")
        
    return wifi_list


# --- API ENDPOINTS ---

@app.get("/")
def read_root():
    """Root route welcoming users to the API."""
    return {
        "message": "Welcome to Akanno Labs SOC API",
        "endpoints": {
            "telemetry": "/api/telemetry",
            "wifi": "/api/wifi",
            "geoip": "/api/geoip/{ip}",
            "threat": "/api/threat/{ip}",
            "docs": "/docs"
        }
    }


@app.get("/api/telemetry")
def get_telemetry():
    """Endpoint fetched by dashboard UI for security logs."""
    refresh_telemetry()
    if os.path.exists(TELEMETRY_FILE):
        with open(TELEMETRY_FILE, "r") as f:
            data = json.load(f)
        return {"status": "success", "total_events": len(data), "events": data}
    return {"status": "error", "message": "Telemetry file not found", "events": []}


@app.get("/api/wifi")
def get_wifi():
    """Endpoint fetched by dashboard UI for saved Wi-Fi networks."""
    data = fetch_wifi_data()
    return {"status": "success", "total_networks": len(data), "networks": data}


@app.get("/api/geoip/{ip}")
def get_ip_geo(ip: str):
    """Endpoint for retrieving real-time Geolocation context."""
    return enrich_ip_location(ip)


@app.get("/api/threat/{ip}")
def get_threat_intel(ip: str):
    """Returns threat score, risk verdict, and ISP metadata for a target IP address."""
    if query_threat_intel:
        return query_threat_intel(ip)
    return {"error": "Threat intelligence module failed to load."}


# --- SERVER RUNNER ---

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Akanno Labs SOC API Server with Threat Intel Gateway...")
    uvicorn.run("api_server:app", host="127.0.0.1", port=8000, reload=True)