from typing import List, Dict, Any, Tuple


SEVERITY_PENALTY = {
    "warning": 5,
    "critical": 15,
}


def calculate_reliability(alerts: List[Dict[str, Any]]) -> Tuple[int, str]:
    """
    Calculate reliability score and mode based on active alerts.
    """
    score = 100

    for alert in alerts:
        severity = alert.get("severity")
        penalty = SEVERITY_PENALTY.get(severity, 0)
        score -= penalty

    score = max(score, 0)

    if score >= 90:
        mode = "stable"
    elif score >= 70:
        mode = "degraded"
    elif score >= 40:
        mode = "unstable"
    else:
        mode = "critical"

    return score, mode
