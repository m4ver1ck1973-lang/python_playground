# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests<3",
#   "rich",
#   "psutil",
# ]
# ///

import platform
import sys
import psutil
import requests
from rich.console import Console
from rich.table import Table

console = Console()

# Fetch IP Address
try:
    resp = requests.get("https://api.ipify.org?format=json", timeout=5)
    resp.raise_for_status()
    ip = resp.json()["ip"]
except requests.RequestException as e:
    console.print(f"[red]Error fetching IP address:[/red] {e}")
    sys.exit(1)

# System Identification
if sys.platform == "win32":
    win_ver = sys.getwindowsversion()
    os_build = "Windows 11" if win_ver.build >= 22000 else "Windows 10"
else:
    os_build = f"{platform.system()} {platform.release()}"

# Hardware Statistics
mem = psutil.virtual_memory()
ram_total = f"{mem.total / (1024 ** 3):.2f} GB"
ram_used = f"{mem.used / (1024 ** 3):.2f} GB"
ram_percent = f"{mem.percent}%"

disk_path = "C:\\" if sys.platform == "win32" else "/"
disk = psutil.disk_usage(disk_path)
disk_total = f"{disk.total / (1024 ** 3):.2f} GB"
disk_used = f"{disk.used / (1024 ** 3):.2f} GB"
disk_usage = f"{disk.percent}%"

# Display Table
table = Table(title="System Stats", padding=(0, 1), min_width=50)

table.add_column("Metric", justify="left", style="bold green")
table.add_column("Value", justify="left", style="cyan")

table.add_row("IP", ip)
table.add_row("OS", os_build, end_section=True)
table.add_row("RAM Total", ram_total)
table.add_row("RAM Used", ram_used)
table.add_row("RAM %", ram_percent, end_section=True)
table.add_row("Disk Total", disk_total)
table.add_row("Disk Used", disk_used)
table.add_row("Disk Usage", disk_usage)

console.print(table)