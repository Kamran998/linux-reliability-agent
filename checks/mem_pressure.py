from typing import Dict, Any, List


def check_memory_pressure(metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Check memory availability levels and return alert descriptors.
    """
    alerts = []

    memory = metrics.get("memory", {})
    available = memory.get("mem_available_percent")

    if available is None:
        return alerts

    if available <= 10:
        alerts.append({
            "source": "mem_pressure",
            "severity": "critical",
            "summary": "Memory availability critically low",
            "details": {
                "mem_available_percent": available
            },
            "tags": ["memory", "capacity"]
        })

    elif available <= 20:
        alerts.append({
            "source": "mem_pressure",
            "severity": "warning",
            "summary": "Memory availability low",
            "details": {
                "mem_available_percent": available
            },
            "tags": ["memory", "capacity"]
        })

    return alerts
