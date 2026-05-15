# VAXINX NetGuard 🛡️
### Network Threat Monitor & Process Inspector

> **Status:** Active Development · **Phase 2 — Real Data Injection** · v2.0 · Python 3.8+ · Windows / Linux

---

## Overview

VAXINX NetGuard is a local network security monitoring tool that scans running processes, open ports, and socket connections — flagging suspicious behavior, logging findings to JSON, and displaying results in a real-time HTML dashboard.

Educational defensive monitoring tool for cybersecurity learning, telemetry visualization, and system architecture experimentation.

Live: https://regislara-byte.github.io/vaxinx-netguard/dashboard/
      https://regislara-byte.github.io/vaxinx-netguard/assets/visualloreartifacts/mascots/brand.html

---

## 🚀 Phase 2 — Real Data Injection

**THIS is the big evolution.**

Phase 2 closes the loop between the Python scanner and the browser dashboard.

```
Python scanner
    ↓  writes
reports/network_report.json
    ↓  fetch()
dashboard/index.html
    ↓  renders
Live alerts · Charts · Process table · Quarantine viewer
```

### What changed in Phase 2

| Feature | Phase 1 | Phase 2 |
|---|---|---|
| Data source | Hardcoded mock JS | `fetch('../reports/network_report.json')` |
| JSON schema | No formal schema | Fully typed, documented schema |
| Auto-refresh | None | Configurable interval (10s / 30s / 1min / 5min) |
| Mock fallback | Always on | Toggleable — shows badge: `LIVE DATA` vs `MOCK DATA` |
| Process paths | None | `exe_path` field per process |
| Threat score | None | Computed ring gauge (0–100) with severity breakdown |
| Connection detail | Minimal | `remote_ip`, `service`, `state`, `mb_sent`, `mb_recv`, `risk` |
| Fetch status | None | Live footer badge per panel: `● Loaded` / `✕ Failed` |
| JSON viewer | Plain text | Syntax highlighted — keys, strings, numbers, threats |
| Timestamp | None | `scan_time`, per-threat `time`, per-alert `time` |

---

## Architecture

```
netguard.py  →  JSON report  →  index.html dashboard
     ↓               ↓                  ↓
  psutil        network_report      live alerts
  scanner         .json log         charts
  engine                            quarantine viewer
```

### Component Map

| Component | File | Role |
|---|---|---|
| Scanner engine | `netguard.py` | Process / port / socket inspection |
| JSON report | `reports/network_report.json` | Structured output — Phase 2 schema |
| Dashboard | `dashboard/index.html` | Real-time browser UI with fetch() |
| Whitelist | `SAFE_PROCESSES` in scanner | Known-safe process names |
| Port map | `COMMON_PORTS` in scanner | Port-to-service labels |

---

## Features

### ✅ v1 (existing)
- [x] psutil-based process enumeration
- [x] JSON report output to `reports/network_report.json`
- [x] Safe process whitelist (`SAFE_PROCESSES`)
- [x] Common port labeling (`COMMON_PORTS`)
- [x] Auto-creates report directory

### ✅ v2 Dashboard (Phase 2 complete)
- [x] **`fetch()` data injection** — reads real `network_report.json` on load
- [x] **Auto-refresh** — configurable interval, countdown timer in header
- [x] **Live / Mock badge** — header badge shows `LIVE DATA` or `MOCK DATA`
- [x] **Fetch status footer** — per-panel status: loaded, failed, loading
- [x] **Mock fallback** — graceful degradation when JSON file unreachable
- [x] **Threat score ring** — animated gauge 0–100 with severity breakdown
- [x] **Process exe_path** — full binary path per process in table
- [x] **Syntax-highlighted JSON viewer** — keys, strings, numbers, threats colored
- [x] **Timestamped alerts** — `time` field rendered per alert and threat
- [x] **Connection risk column** — `risk` field flags suspicious sockets
- [x] **Live alert feed** — severity-ranked (Critical / High / Medium / Low)
- [x] **Real-time traffic chart** — inbound/outbound bytes/s, live-updating
- [x] **Threat breakdown chart** — doughnut by category
- [x] **Quarantine viewer** — review, release, or delete quarantined items
- [x] **Process monitor table** — CPU%, MEM%, connection count, one-click quarantine
- [x] **Port map** — visual grid: open / suspicious / well-known
- [x] **Socket connection table** — local:remote with state + risk badges
- [x] **Live activity log** — streaming event feed with INFO / WARN / THREAT / FETCH levels
- [x] **Scan progress bar** — animated scan lifecycle indicator
- [x] **Network traffic analysis** — bandwidth over time + protocol breakdown
- [x] **Alert banner** — top-of-page threat notification strip

---

## Installation

```bash
# Clone / download
cd vaxinx-netguard

# Install dependency
pip install psutil

# Run scanner (generates network_report.json)
python netguard.py

# Open dashboard (must be served, not file:// for fetch() to work)
python -m http.server 8080
# then open: http://localhost:8080/dashboard/
```

> **Important for Phase 2:** `fetch()` requires a server context.
> Running `index.html` directly via `file://` will trigger CORS restrictions.
> Use `python -m http.server 8080` or VS Code Live Server.

---

## Usage

### Basic Scan
```bash
python netguard.py
```
Outputs `reports/network_report.json`. Open dashboard to view results.

### Watch Mode (auto-rescan)
```bash
python netguard.py --watch --interval 30
```
Re-scans every 30 seconds. Dashboard auto-refreshes to match.

### Custom output path
```bash
python netguard.py --output /tmp/scan.json
```

---

## JSON Schema (v2)

The dashboard reads this exact structure from `reports/network_report.json`:

```json
{
  "scan_time":        "ISO 8601 timestamp",
  "scanner_version":  "string",
  "host":             "machine hostname",
  "platform":         "OS version string",

  "summary": {
    "total_processes": 47,
    "safe":            44,
    "threats":          2,
    "quarantined":      2,
    "open_ports":      14,
    "suspicious_ports": 3,
    "scan_duration_ms": 1842
  },

  "threat_score": {
    "total":    72,
    "critical":  1,
    "high":      1,
    "medium":    1,
    "low":       2
  },

  "processes": [{
    "pid":          3344,
    "name":         "netcat.exe",
    "cpu_percent":  0.5,
    "mem_percent":  0.8,
    "connections":  5,
    "exe_path":     "C:\\Users\\...\\nc.exe",
    "status":       "threat"
  }],

  "threats": [{
    "pid":    3344,
    "name":   "netcat.exe",
    "risk":   "CRITICAL",
    "reason": "Reverse shell signature…",
    "action": "quarantined",
    "time":   "ISO 8601"
  }],

  "alerts": [{
    "severity": "critical",
    "title":    "Reverse shell attempt detected",
    "details":  "PID 3344 · netcat.exe · port 4444",
    "time":     "ISO 8601"
  }],

  "ports": {
    "suspicious": [4444, 1337, 31337],
    "open":       [8080, 3306, 5432],
    "known":      [80, 443, 53, 22]
  },

  "connections": [{
    "remote_ip":   "192.168.1.45",
    "remote_port": 9001,
    "service":     "C2?",
    "local_addr":  "0.0.0.0:4444",
    "protocol":    "TCP",
    "state":       "ESTABLISHED",
    "process":     "netcat.exe",
    "mb_sent":     3.2,
    "mb_recv":     0.4,
    "risk":        "critical"
  }],

  "safe_processes": ["chrome.exe", "svchost.exe", "..."]
}
```

---

## Dashboard Pages

| Page | What it shows |
|---|---|
| **Dashboard** | Stats, threat score ring, scan status, traffic chart, live log |
| **Live Alerts** | Severity-ranked alerts with timestamps from JSON |
| **Processes** | All processes with CPU/mem/path/conns + quarantine action |
| **Ports / Sockets** | Open, suspicious, known ports + full socket connection table |
| **Network Traffic** | Bandwidth chart, top connections by volume, protocol mix |
| **Quarantine** | Quarantined items from JSON — release or delete |
| **JSON Logs** | Syntax-highlighted `network_report.json` inline |
| **Settings** | Auto-refresh toggle, interval, mock fallback toggle |

---

## Threat Detection Logic

### Suspicious Process Signals
- Process name not in `SAFE_PROCESSES` whitelist
- Excessive outbound connections (> configurable threshold)
- CPU or memory spikes above baseline
- Process spawned from unusual parent (`cmd.exe` → unknown binary)
- Binary in suspicious path (`%TEMP%`, `%APPDATA%`, `ProgramData`)
- Unsigned executable

### Suspicious Port Signals
- Known attack / C2 ports: `4444`, `1337`, `31337`, `9001`, `6666`, `4899`, `5900`
- Unusual listening socket with no matching service
- Port bound by a process mismatching expected service

### Alert Severity Levels
| Level | Criteria |
|---|---|
| 🔴 Critical | Confirmed signature match, active reverse shell, known RAT |
| 🟡 High | Anomalous behavior with multiple strong indicators |
| 🔵 Medium | Unusual but inconclusive activity |
| 🟢 Low | Informational — new process, port change, parent change |

### Threat Score Calculation
```
score = (critical × 40) + (high × 20) + (medium × 8) + (low × 2)
capped at 100
```

---

## Project Structure

```
vaxinx-netguard/
├── netguard.py                  # Scanner engine
├── dashboard/
│   └── index.html               # Phase 2 dashboard — fetch() powered
├── reports/
│   └── network_report.json      # Real scan output (v2 schema)
├── assets/
│   └── visualloreartifacts/     # VLA — project evolution screenshots
│       ├── phase1/              # First dashboard, scanner v1
│       ├── phase2/              # Real data injection, fetch() integration
│       ├── phase3/              # (upcoming)
│       └── phase4/              # (upcoming)
└── README.md
```

---

## VLA — Visual Lore Artifacts

VLA captures the engineering evolution of VAXINX NetGuard through visual proof snapshots.

- Phase 1: static dashboard, first UI, setup flow
- Phase 2: real JSON export, fetch connection, auto-refresh, live dashboard, terminal scan
- Architecture: folder tree, VS Code structure, dashboard layout, scan flow

Path:

```
assets/visualloreartifacts/
```

Documents: dashboard evolution · scanner progression · JSON integration ·
live alert development · frontend architecture phases · AI-assisted engineering workflow.

---

## Roadmap

### Phase 3 (next)
- [ ] `--watch` mode writing JSON on interval (Python side)
- [ ] WebSocket or SSE for true real-time push (no polling)
- [ ] Historical scan diff view — delta between scans

### Phase 4
- [ ] Email / webhook alert dispatch on Critical findings
- [ ] YARA rule signature database integration
- [ ] Docker container for isolated scanning
- [ ] Remote host scanning via SSH tunnel
- [ ] CVE lookup for detected service versions

---

## Dependencies

| Package | Purpose |
|---|---|
| `psutil` | Process, port, and connection enumeration |
| `json` | Report serialization (stdlib) |
| `pathlib` | File path handling (stdlib) |
| `datetime` | Scan timestamps (stdlib) |

Dashboard: **zero server-side dependencies** — pure HTML/CSS/JS, Chart.js via CDN.

---

## ⚠️ Cybersecurity Assessment

See `SECURITY_ASSESSMENT.md` for full analysis of detection capabilities, limitations, and upgrade recommendations.

**Summary ratings:**

| Capability | Rating |
|---|---|
| Process enumeration | ✅ Functional |
| Port scanning | ✅ Functional |
| Signature detection | ⚠️ Heuristic (name/port match) |
| Behavioral analysis | 🔲 Roadmap |
| Real-time alerting | ✅ Dashboard (poll-based) |
| Quarantine action | ⚠️ UI only — no OS-level isolation yet |
| Evasion resistance | 🔲 Roadmap |

---

## License

MIT — use freely, contribute back.
