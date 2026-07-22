import React, { useState, useEffect } from 'react';

export default function Dashboard() {
  const [telemetry, setTelemetry] = useState([]);
  const [wifiNetworks, setWifiNetworks] = useState([]);
  const [loading, setLoading] = useState(true);

  // Define API endpoint (Use ngrok URL if running Bolt.new in cloud)
  const API_BASE = "http://127.0.0.1:8000";

  const fetchSOCData = async () => {
    setLoading(true);
    try {
      // Fetch Security Telemetry
      const telRes = await fetch(`${API_BASE}/api/telemetry`);
      const telData = await telRes.json();
      if (telData.status === "success") {
        setTelemetry(telData.events);
      }

      // Fetch Saved Wi-Fi Profiles
      const wifiRes = await fetch(`${API_BASE}/api/wifi`);
      const wifiData = await wifiRes.json();
      if (wifiData.status === "success") {
        setWifiNetworks(wifiData.networks);
      }
    } catch (error) {
      console.error("API Fetch Error:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSOCData();
  }, []);

  return (
    <div className="p-6 bg-slate-900 text-cyan-400 font-mono min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold tracking-widest text-cyan-300">
          NEURAL_NET SOC v4.0 // LIVE ENGINE
        </h1>
        <button 
          onClick={fetchSOCData}
          className="px-4 py-2 bg-pink-600 hover:bg-pink-700 text-white rounded font-semibold transition"
        >
          {loading ? "REFRESHING..." : "SYNC API DATA"}
        </button>
      </div>

      {/* Telemetry Stream */}
      <section className="mb-8 border border-cyan-800 rounded p-4 bg-slate-950">
        <h2 className="text-lg font-semibold mb-3 text-pink-500">
          [🚨] SECURITY EVENT TELEMETRY ({telemetry.length})
        </h2>
        <div className="space-y-2">
          {telemetry.map((evt, idx) => (
            <div key={idx} className="p-3 border border-slate-800 bg-slate-900 rounded flex justify-between items-center">
              <div>
                <span className="text-xs bg-pink-900 text-pink-200 px-2 py-0.5 rounded mr-2">
                  {evt.event_type}
                </span>
                <span className="text-slate-300">IP: {evt.source_ip}</span>
              </div>
              <span className="text-xs text-slate-500">{evt.timestamp}</span>
            </div>
          ))}
        </div>
      </section>

      {/* Wi-Fi Credentials Stream */}
      <section className="border border-cyan-800 rounded p-4 bg-slate-950">
        <h2 className="text-lg font-semibold mb-3 text-cyan-400">
          [📶] SAVED WI-FI CREDENTIALS ({wifiNetworks.length})
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {wifiNetworks.map((net, idx) => (
            <div key={idx} className="p-3 border border-slate-800 bg-slate-900 rounded">
              <p className="text-cyan-300 font-bold">SSID: {net.ssid}</p>
              <p className="text-sm text-slate-400">KEY: <span className="text-pink-400">{net.password}</span></p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}