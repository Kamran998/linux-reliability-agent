import os
import shutil
import time
from typing import Dict, Any


def _disk_usage_percent(path: str) -> float:
    usage = shutil.disk_usage(path)
    return round((usage.used / usage.total) * 100, 2)


def _mem_available_percent() -> float:
    mem_total = None
    mem_available = None

    with open("/proc/meminfo", "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("MemTotal:"):
                mem_total = int(line.split()[1])
            elif line.startswith("MemAvailable:"):
                mem_available = int(line.split()[1])

    if not mem_total or not mem_available:
        return 0.0

    return round((mem_available / mem_total) * 100, 2)


def _uptime_seconds() -> int:
    with open("/proc/uptime", "r", encoding="utf-8") as f:
        return int(float(f.read().split()[0]))


def collect_sys_metrics() -> Dict[str, Any]:
    """
    Collect core Linux reliability metrics.
    This function must never raise.
    """
    try:
        metrics = {
            "timestamp": int(time.time()),
            "uptime_seconds": _uptime_seconds(),
            "cpu": {
                "cores": os.cpu_count() or 0,
                "load_1": os.getloadavg()[0],
                "load_5": os.getloadavg()[1],
                "load_15": os.getloadavg()[2],
            },
            "memory": {
                "mem_available_percent": _mem_available_percent(),
            },
            "disk": {
                "root_percent": _disk_usage_percent("/"),
                "var_percent": _disk_usage_percent("/var") if os.path.exists("/var") else None,
            },
        }

        return metrics

    except Exception:
        # Always return a dict, even on failure
        return {
            "timestamp": int(time.time()),
            "error": "metric_collection_failed",
        }
