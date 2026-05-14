# VAXINX NetGuard 🛡️
### Network Threat Monitor & Process Inspector

> **Status:** Active Development · v2.0 · Python 3.8+ · Windows / Linux

---

## Overview

VAXINX NetGuard is a local network security monitoring tool that scans running processes, open ports, and socket connections — flagging suspicious behavior, logging findings to JSON, and displaying results in a real-time HTML dashboard.

Educational defensive monitoring tool for cybersecurity learning, telemetry visualization, and system architecture experimentation.

It is designed as a lightweight, dependency-minimal first-response tool: run it on any machine in seconds, get a structured report, and review threats in the browser.

---

Live : https://regislara-byte.github.io/vaxinx-netguard/dashboard/

## Architecture

```
netguard.py  →  JSON report  →  index.html dashboard
     ↓               ↓                  ↓
  psutil        network_report      live alerts
  scanner         .json log         charts
  engine                            quarantine viewer
```

---
### Component Map

| Component | File | Role |
|---|---|---|
| Scanner engine | `netguard.py` | Process / port / socket inspection |
| JSON report | `reports/network_report.json` | Structured output log |
| Dashboard | `dashboard/index.html` | Real-time browser UI |
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

### 🆕 v2 Dashboard Upgrades
- [x] **Live alert feed** — severity-ranked (Critical / High / Medium / Low)
- [x] **Real-time traffic chart** — inbound/outbound bytes/s, live-updating
- [x] **Threat breakdown chart** — doughnut by category (reverse shell, anomalous conn, port abuse)
- [x] **Quarantine viewer** — review, release, or delete quarantined items
- [x] **Process monitor table** — CPU%, MEM%, connection count, one-click quarantine
- [x] **Port map** — visual grid: open / suspicious / well-known
- [x] **Socket connection table** — local:remote with state badges
- [x] **JSON log viewer** — formatted `network_report.json` inline
- [x] **Live activity log** — streaming event feed with INFO / WARN / THREAT levels
- [x] **Scan progress bar** — animated scan lifecycle indicator
- [x] **Network traffic analysis** — bandwidth over time + protocol breakdown
- [x] **Alert banner** — top-of-page threat notification strip

---

## Installation

```bash
# Clone / download the project
cd vaxinx-netguard

# Install dependency
pip install psutil

# Run scanner
python netguard.py

# Open dashboard
start dashboard/index.html    # Windows
open dashboard/index.html     # macOS
xdg-open dashboard/index.html # Linux
```

---

## Usage

### Basic Scan
```bash
python netguard.py
```
Outputs `reports/network_report.json` and prints summary to terminal.

### Watch Mode (continuous)
```bash
python netguard.py --watch --interval 30
```
Re-scans every 30 seconds. Dashboard auto-reloads via polling.

### Export to different path
```bash
python netguard.py --output /tmp/scan_results.json
```

---

## Dashboard Pages

| Page | What it shows |
|---|---|
| **Dashboard** | Stats overview, scan status, traffic + threat charts, live log |
| **Live Alerts** | All alerts sorted by severity with timestamps |
| **Processes** | All running processes with CPU/mem/conn stats + quarantine button |
| **Ports / Sockets** | Open, suspicious, and well-known ports; socket connection table |
| **Network Traffic** | Bandwidth over time, top connections by volume, protocol mix |
| **Quarantine** | Quarantined items — release or delete with audit trail |
| **JSON Logs** | Raw `network_report.json` formatted inline |
| **Settings** | Toggle scan targets, view whitelist |

---

## Threat Detection Logic

### Suspicious Process Signals
- Process name not in `SAFE_PROCESSES` whitelist
- Process has high number of outbound connections (> configurable threshold)
- Process CPU or memory usage spikes above baseline
- Process spawned from unusual parent (e.g. `cmd.exe` → unknown binary)

### Suspicious Port Signals
- Known attack/C2 ports: `4444`, `1337`, `31337`, `9001`, `6666`
- Unusual listening socket with no known associated service
- Port bound by a process not matching expected service

### Alert Severity Levels
| Level | Criteria |
|---|---|
| 🔴 Critical | Confirmed malware signature or active reverse shell |
| 🟡 High | Anomalous behavior with strong threat indicators |
| 🔵 Medium | Unusual but inconclusive activity |
| 🟢 Low | Informational — new process, port opened, etc. |

---

## JSON Report Format

```json
{
  "scan_time": "2025-05-14T14:22:08",
  "host": "HOSTNAME",
  "scanner": "vaxinx-netguard v2.0",
  "summary": {
    "total_processes": 47,
    "threats": 2,
    "quarantined": 2,
    "open_ports": 14
  },
  "threats": [
    {
      "pid": 3344,
      "name": "netcat.exe",
      "risk": "CRITICAL",
      "reason": "Reverse shell signature detected · port 4444 outbound",
      "action": "quarantined"
    }
  ],
  "safe_processes": ["chrome.exe", "svchost.exe", "..."],
  "ports": {
    "suspicious": [4444, 1337, 31337],
    "open": [8080, 3306, 5432, 8443],
    "known": [80, 443, 53, 22]
  }
}
```

---

## Project Structure

```
vaxinx-netguard/
├── netguard.py              # Scanner engine
├── dashboard/
│   └── index.html           # Dashboard UI
├── reports/
│   └── network_report.json  # Auto-generated scan output
└── README.md
```

---

## Visual Lore Artifacts (VLA)

Project evolution screenshots, debugging milestones, UI transitions, and architecture states are stored under:

assets/visualloreartifacts/

These artifacts document:
- dashboard evolution
- scanner progression
- JSON integration
- live alert development
- frontend architecture phases
- AI-assisted engineering workflow

```txt
assets/
└── visualloreartifacts/
    ├── phase1/
    ├── phase2/
    ├── phase3/
    └── phase4/

---

## Roadmap

- [ ] `--watch` mode with auto-dashboard refresh
- [ ] Email / webhook alert dispatch on Critical findings
- [ ] Signature database (YARA rule support)
- [ ] Historical scan comparison / diff view
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

See `SECURITY_ASSESSMENT.md` for full analysis of detection capabilities, limitations, and recommendations.

---

## License

MIT — use freely, contribute back.
