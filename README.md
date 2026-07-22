# 🛡️ Akanno Security Labs — Automated SOC & SIEM Engine

An end-to-end, modular Python Security Operations Center (SOC) telemetry pipeline featuring real-time log ingestion, packet sniffing, GeoIP enrichment, automated firewall mitigation (SOAR), multi-channel alert dispatch, and executive PDF reporting.

---

## 🏗️ Architecture & Data Pipeline

```text
[ Network Logs / Packets ] ──> [ SOC Detection Engine ] ──> [ FastAPI REST Server ] ──> [ Cyberpunk Web UI ]
                                       │                            │
                                       ├──> [ GeoIP Enricher ]      ├──> [ Discord Webhook Alerts ]
                                       │                            │
                                       └──> [ Firewall Response ]   └──> [ Executive PDF Generator ]