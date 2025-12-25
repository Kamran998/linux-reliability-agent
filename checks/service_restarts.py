import subprocess
import time
from typing import Dict, Any, List

SERVICES = [
    "sshd",
    "NetworkManager",
    "chronyd",
    "rsyslog",
]

WINDOW_SECONDS = 600  # 10 minutes


def _get_restart_count(service: str) -> int:
    """
    Return NRestarts from systemd for a service.
    """
    try:
        result = subprocess.run(
            ["systemctl", "show", service, "--property=NRestarts"],
            capture_output=True,
            text=True,
            timeout=2,
        )
        if result.returncode != 0:
            return 0

        value = result.stdout.strip().split("=")[-1]
        return int(value)
    except Exception:
        return 0


def check_service_restarts(metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Detect service restart instability.
    """
    alerts = []
    now = int(time.time())

    for service in SERVICES:
        restarts = _get_restart_count(service)

        if restarts >= 5:
            alerts.append({
                "source": "service_restarts",
                "severity": "critical",
                "summary": f"Service {service} restarting frequently",
                "details": {
                    "service": service,
                    "restart_count": restarts,
                    "window_seconds": WINDOW_SECONDS,
                    "timestamp": now,
                },
                "tags": ["service", "restart", "stability"],
            })

        elif restarts >= 3:
            alerts.append({
                "source": "service_restarts",
                "severity": "warning",
                "summary": f"Service {service} showing restart instability",
                "details": {
                    "service": service,
                    "restart_count": restarts,
                    "window_seconds": WINDOW_SECONDS,
                    "timestamp": now,
                },
                "tags": ["service", "restart", "stability"],
            })

    return alerts
