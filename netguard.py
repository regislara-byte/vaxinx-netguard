"""
VAXINX NetGuard v1
Educational defensive network/process monitor.
Generates a JSON report for the dashboard.
"""

import json
import time
from pathlib import Path
from datetime import datetime

try:
    import psutil
except ImportError:
    print("Missing module: psutil")
    print("Install it with: pip install psutil")
    exit()


BASE_DIR = Path(__file__).resolve().parent
REPORT_DIR = BASE_DIR / "reports"
REPORT_FILE = REPORT_DIR / "network_report.json"

REPORT_DIR.mkdir(exist_ok=True)

SAFE_PROCESSES = {
    "chrome.exe",
    "msedge.exe",
    "firefox.exe",
    "explorer.exe",
    "svchost.exe",
    "python.exe",
    "code.exe"
}

COMMON_PORTS = {
    80: "HTTP web traffic",
    443: "HTTPS secure web traffic",
    53: "DNS lookup",
    22: "SSH remote access",
    3389: "Remote Desktop",
    3306: "MySQL database",
    5432: "PostgreSQL database"
}


def mb(bytes_value):
    return round(bytes_value / (1024 * 1024), 2)


def get_network_speed():
    sent_1 = psutil.net_io_counters().bytes_sent
    recv_1 = psutil.net_io_counters().bytes_recv

    time.sleep(1)

    sent_2 = psutil.net_io_counters().bytes_sent
    recv_2 = psutil.net_io_counters().bytes_recv

    return {
        "upload_mb_per_sec": mb(sent_2 - sent_1),
        "download_mb_per_sec": mb(recv_2 - recv_1),
        "total_uploaded_mb": mb(sent_2),
        "total_downloaded_mb": mb(recv_2)
    }


def get_processes():
    processes = []

    for proc in psutil.process_iter(["pid", "name"]):
        try:
            name = proc.info["name"] or "unknown"
            name_lower = name.lower()

            if name_lower in SAFE_PROCESSES:
                risk = "LOW"
                meaning = "Known or common process."
            else:
                risk = "MEDIUM"
                meaning = "Unknown process. Review if unfamiliar."

            processes.append({
                "pid": proc.info["pid"],
                "name": name,
                "risk": risk,
                "meaning": meaning
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return processes[:40]


def get_ports():
    ports = []

    for conn in psutil.net_connections(kind="inet"):
        try:
            if conn.laddr:
                port = conn.laddr.port
                meaning = COMMON_PORTS.get(port, "Unmapped local port")

                risk = "LOW"

                if port in [22, 3389, 3306, 5432]:
                    risk = "MEDIUM"

                ports.append({
                    "ip": conn.laddr.ip,
                    "port": port,
                    "status": conn.status,
                    "meaning": meaning,
                    "risk": risk
                })

        except Exception:
            continue

    return ports[:30]


def analyze_risk(network, processes, ports):
    score = 0
    alerts = []

    if network["upload_mb_per_sec"] > 5:
        score += 50
        alerts.append("High upload activity detected.")

    if network["download_mb_per_sec"] > 10:
        score += 30
        alerts.append("High download activity detected.")

    unknown_processes = [p for p in processes if p["risk"] == "MEDIUM"]

    if len(unknown_processes) > 10:
        score += 20
        alerts.append("Many unknown processes detected.")

    sensitive_ports = [p for p in ports if p["risk"] == "MEDIUM"]

    if sensitive_ports:
        score += 20
        alerts.append("Sensitive local port detected.")

    if score >= 70:
        level = "HIGH"
        action = "Investigate now."
    elif score >= 30:
        level = "MEDIUM"
        action = "Monitor closely."
    else:
        level = "LOW"
        action = "Normal activity. Keep observing."

    if not alerts:
        alerts.append("No major warning detected.")

    return {
        "level": level,
        "score": score,
        "recommended_action": action,
        "alerts": alerts
    }


def build_report():
    network = get_network_speed()
    processes = get_processes()
    ports = get_ports()
    risk = analyze_risk(network, processes, ports)

    return {
        "tool": "VAXINX NetGuard v1",
        "mode": "Defensive Learning Monitor",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "network": network,
        "risk": risk,
        "processes": processes,
        "ports": ports
    }


def save_report(report):
    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)


def main():
    report = build_report()
    save_report(report)

    print("🛡️ VAXINX NetGuard v1 Complete")
    print("Report:", REPORT_FILE)
    print("Risk:", report["risk"]["level"])
    print("Score:", report["risk"]["score"])
    print("Action:", report["risk"]["recommended_action"])


if __name__ == "__main__":
    main()
    