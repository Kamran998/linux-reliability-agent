from typing import Dict, Any, List


def check_disk_pressure(metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Check disk usage levels and return alert descriptors.
    """
    alerts = []

    disk = metrics.get("disk", {})
    for mount, percent in disk.items():
        if percent is None:
            continue

        if percent >= 90:
            alerts.append({
                "source": "disk_pressure",
                "severity": "critical",
                "summary": f"Disk usage critical on {mount}",
                "details": {
                    "mount": mount,
                    "usage_percent": percent
                },
                "tags": ["disk", "capacity"]
            })

        elif percent >= 85:
            alerts.append({
                "source": "disk_pressure",
                "severity": "warning",
                "summary": f"Disk usage high on {mount}",
                "details": {
                    "mount": mount,
                    "usage_percent": percent
                },
                "tags": ["disk", "capacity"]
            })

    return alerts
