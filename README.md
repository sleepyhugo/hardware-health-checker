# Hardware Health & Inventory Checker (Python)

A simple Python CLI tool that collects basic system hardware/OS information, runs quick health checks, and logs results for inventory-style tracking.

## Features
- Collects system info: OS, CPU cores, RAM usage, disk usage
- Basic health warnings (high disk usage, low available RAM)
- Appends each run to a JSON log file (`hardware_log.json`)
- Menu options to view recent logs and export the latest report (`latest_report.txt`)

## Requirements
- Python 3.x
- `psutil`

Install dependency:  
`python -m pip install psutil`

## Run
`python hardware_checker.py`

## Output Files  
- `hardware_log.json` - stores a history of system snapshots + warnings
- `latest_report.txt` - exported text report from the most recent run

## Notes  
This is a lightweight, beginner-friendly project meant to demonstrate basic monitoring, documentation, and repeatable health checks similar to lab or hardware farm workflows.

