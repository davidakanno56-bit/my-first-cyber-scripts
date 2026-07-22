import json
import urllib.request

# ==========================================
# CONFIGURATION
# ==========================================
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1529492055313617111/swzBNieDchjGIoJTq4ORVO_tzIKSIff2g3sCVOmO2SJl3x9ayfCU-QWU1QxR8kLVrLra"


def send_discord_alert(event_type: str, severity: str, source_ip: str, message: str):
    """Formats and sends a rich alert embed to a Discord Webhook channel."""
    
    # Choose decimal border color based on severity
    color_map = {
        "CRITICAL": 15158332,  # Neon Red
        "HIGH": 15105570,      # Orange
        "MEDIUM": 16776960,    # Yellow
        "INFO": 3066993        # Cyan
    }
    
    embed_color = color_map.get(severity.upper(), 3066993)

    payload = {
        "username": "Akanno SOC Sentinel",
        "embeds": [
            {
                "title": f"🚨 SOC THREAT ALERT: [{severity.upper()}]",
                "description": f"**Event:** {event_type}\n**Details:** {message}",
                "color": embed_color,
                "fields": [
                    {
                        "name": "Target / Source IP",
                        "value": f"`{source_ip}`",
                        "inline": True
                    },
                    {
                        "name": "Action Status",
                        "value": "`ACTION REQUIRED`" if severity.upper() in ["CRITICAL", "HIGH"] else "`LOGGED`",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "Akanno Security Labs // SOC Automated Response Engine"
                }
            }
        ]
    }

    # Encode payload to UTF-8 bytes
    data = json.dumps(payload).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        req = urllib.request.Request(
            DISCORD_WEBHOOK_URL,
            data=data,
            headers=headers,
            method="POST"
        )
        with urllib.request.urlopen(req) as response:
            if response.status in [200, 204]:
                print(f"[✅] Discord Alert Sent: {event_type} from {source_ip}")
            else:
                print(f"[!] Discord API Status: {response.status}")
    except Exception as e:
        print(f"[❌] Failed to dispatch Discord alert: {e}")


if __name__ == "__main__":
    print("=" * 55)
    print("      AKANNO LABS - SOC DISPATCH ALERT ENGINE")
    print("=" * 55 + "\n")

    print("[*] Triggering test alert dispatch...")
    send_discord_alert(
        event_type="Port Scan Detected",
        severity="CRITICAL",
        source_ip="192.168.1.105",
        message="Rapid sequential connection attempts across 15 target ports within 3 seconds."
    )