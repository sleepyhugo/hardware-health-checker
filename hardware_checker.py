import json
import platform
from datetime import datetime
from pathlib import Path

import psutil

LOG_FILE = Path("hardware_log.json")


def bytes_to_gb(num_bytes: int) -> float:
    return round(num_bytes / (1024 ** 3), 2)


# Collects system info
def collect_system_info() -> dict:
    # Cpu
    cpu_logical = psutil.cpu_count(logical=True)
    cpu_physical = psutil.cpu_count(logical=False)

    # OS
    os_name = platform.system()
    os_version = platform.version()
    machine = platform.machine()

    # Ram
    vm = psutil.virtual_memory()
    ram_total_gb = bytes_to_gb(vm.total)
    ram_available_gb = bytes_to_gb(vm.available)
    ram_percent_used = vm.percent

    # Disk usage
    disk_path = Path.cwd().anchor or "/"  # Disk path: Windows drive anchor or "/" on Linux/mac
    du = psutil.disk_usage(disk_path)
    disk_total_gb = bytes_to_gb(du.total)
    disk_used_gb = bytes_to_gb(du.used)
    disk_free_gb = bytes_to_gb(du.free)
    disk_percent_used = du.percent

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "os": {"name": os_name, "version": os_version, "arch": machine},
        "cpu": {"physical_cores": cpu_physical, "logical_cores": cpu_logical},
        "ram_gb": {
            "total": ram_total_gb,
            "available": ram_available_gb,
            "percent_used": ram_percent_used,
        },
        "disk_gb": {
            "path_checked": disk_path,
            "total": disk_total_gb,
            "used": disk_used_gb,
            "free": disk_free_gb,
            "percent_used": disk_percent_used,
        },
    }


# Health checks (warnings)
def health_checks(info: dict) -> list[str]:
    warnings: list[str] = []

    if info["disk_gb"]["percent_used"] >= 85:
        warnings.append("Disk usage is high (>= 85%). Consider freeing space.")
    if info["ram_gb"]["available"] <= 2.0:
        warnings.append("RAM available is low (<= 2 GB). Close apps or add memory.")

    return warnings


# Read log
def read_log() -> list[dict]:
    if not LOG_FILE.exists():
        return []
    try:
        data = json.loads(LOG_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


# Write log
def write_log(entries: list[dict]) -> None:
    LOG_FILE.write_text(json.dumps(entries, indent=2), encoding="utf-8")


# Append
def append_log(entry: dict) -> None:
    entries = read_log()
    entries.append(entry)
    write_log(entries)


# Builds a .txt report
def format_report(info: dict, warnings: list[str]) -> str:
    lines = []
    lines.append("=== Hardware Health Report ===")
    lines.append(f"Timestamp: {info['timestamp']}")
    lines.append(f"OS: {info['os']['name']} {info['os']['version']} ({info['os']['arch']})")
    lines.append(
        f"CPU Cores: {info['cpu']['physical_cores']} physical / {info['cpu']['logical_cores']} logical"
    )
    lines.append(
        f"RAM: {info['ram_gb']['available']} GB available / {info['ram_gb']['total']} GB total "
        f"({info['ram_gb']['percent_used']}% used)"
    )
    lines.append(
        f"Disk ({info['disk_gb']['path_checked']}): {info['disk_gb']['free']} GB free / {info['disk_gb']['total']} GB total "
        f"({info['disk_gb']['percent_used']}% used)"
    )

    if warnings:
        lines.append("")
        lines.append("--- Warnings ---")
        for w in warnings:
            lines.append(f"- {w}")
    else:
        lines.append("")
        lines.append("No warnings. System looks healthy for basic checks.")

    return "\n".join(lines)


# Run health check
def run_health_check() -> None:
    info = collect_system_info()
    warnings = health_checks(info)

    entry = {
        "system_info": info,
        "warnings": warnings,
    }

    report = format_report(info, warnings)
    print("\n" + report + "\n")

    append_log(entry)
    print(f"Saved log entry to: {LOG_FILE.resolve()}\n")


# View recent logs
def view_recent_logs(limit: int = 5) -> None:
    entries = read_log()
    if not entries:
        print("\nNo log entries found yet.\n")
        return

    recent = entries[-limit:]
    print(f"\n=== Showing last {len(recent)} log entries ===\n")
    for i, entry in enumerate(recent, start=1):
        info = entry.get("system_info", {})
        ts = info.get("timestamp", "unknown")
        disk = info.get("disk_gb", {}).get("percent_used", "?")
        ram = info.get("ram_gb", {}).get("percent_used", "?")
        warn_count = len(entry.get("warnings", []))
        print(f"{i}. {ts} | Disk Used: {disk}% | RAM Used: {ram}% | Warnings: {warn_count}")
    print("")


# Export latest report
def export_latest_report() -> None:
    entries = read_log()
    if not entries:
        print("\nNo logs found. Run a health check first.\n")
        return

    latest = entries[-1]
    info = latest.get("system_info", {})
    warnings = latest.get("warnings", [])
    report = format_report(info, warnings)

    out_file = Path("latest_report.txt")
    out_file.write_text(report, encoding="utf-8")

    print(f"\nExported latest report to: {out_file.resolve()}\n")


# Menu loop
def menu() -> None:
    while True:
        print("Hardware Health & Inventory Checker")
        print("1) Run health check (collect + log)")
        print("2) View recent logs")
        print("3) Export latest report (txt)")
        print("4) Quit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            run_health_check()
        elif choice == "2":
            view_recent_logs()
        elif choice == "3":
            export_latest_report()
        elif choice == "4":
            print("\nGoodbye!\n")
            break
        else:
            print("\nInvalid option. Try again.\n")


if __name__ == "__main__":
    menu()
