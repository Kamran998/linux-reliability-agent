from typing import Dict, Any, List


def check_load_pressure(metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Check CPU load normalized by core count.
    """
    alerts = []

    cpu = metrics.get("cpu", {})
    load_1 = cpu.get("load_1")
    cores = cpu.get("cores")

    if not load_1 or not cores:
        return alerts

    normalized = round(load_1 / cores, 2)

    if normalized >= 2.0:
        alerts.append({
            "source": "load_pressure",
            "severity": "critical",
            "summary": "Sustained CPU load critically high",
            "details": {
                "load_1": load_1,
                "cores": cores,
                "normalized_load": normalized
            },
            "tags": ["cpu", "load"]
        })

    elif normalized >= 1.2:
        alerts.append({
            "source": "load_pressure",
            "severity": "warning",
            "summary": "Sustained CPU load high",
            "details": {
                "load_1": load_1,
                "cores": cores,
                "normalized_load": normalized
            },
            "tags": ["cpu", "load"]
        })

    return alerts
