# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests<3",
#   "rich",
#   "psutil"
# ]
# ///

import platform
import psutil
import sys
import requests
from rich.console import Console
from rich.table import Table

console = Console()

# Fetch
resp = requests.get("https://api.ipify.org?format=json")
status = resp.status_code
if status != 200:
    print(f"[red]Error fetching IP address: {status}[/red]")
    exit(1)
else:
    ip = f"{resp.json()['ip']}"
    
# System Identification
win_ver = sys.getwindowsversion()
build_number = win_ver.build
# Distinguish Windows 10 vs 11
if build_number >= 22000:
    os_build = "Windows 11"
else:
    os_build = "Windows 10"

# Hardware Statistics
# 1. Get Memory Stats
mem = psutil.virtual_memory()
ram_total_gb = mem.total / (1024 ** 3)
ram_used_gb = mem.used / (1024 ** 3)
ram_percent = mem.percent

ram_total = f"{ram_total_gb:.2f} GB"
ram_used = f"{ram_used_gb:.2f} GB"
ram_percent = f"{ram_percent}%"

# 2. Get Disk Stats (Windows usually uses 'C:\\')
disk = psutil.disk_usage('C:\\')
disk_total_gb = disk.total / (1024 ** 3)
disk_used_gb = disk.used / (1024 ** 3)
disk_percent = disk.percent

disk_total = f"{disk_total_gb:.2f} GB"
disk_used = f"{disk_used_gb:.2f} GB"
disk_usage = f"{disk_percent}%"

# Display the information in a table using Rich

table = Table(title="Windows Stats", padding=(0,1), min_width=50)

table.add_column("Metric", justify="left", style="bold green")
table.add_column("Value", justify="left", style="cyan")

# Add dynamic data
table.add_row("IP", ip)
table.add_row("OS",os_build, end_section=True)
table.add_row("RAM Total", ram_total)
table.add_row("RAM Used", ram_used)
table.add_row("RAM %", ram_percent, end_section=True)
table.add_row("Disk Total", disk_total)
table.add_row("Disk Used", disk_used)
table.add_row("Disk Usage", disk_usage)

console.print(table)