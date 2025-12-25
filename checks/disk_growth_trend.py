from typing import Dict, Any, List
from checks.trend_analysis import record_metric, calculate_rate


WARNING_RATE = 0.00083     # % per second
CRITICAL_RATE = 0.00167   # % per second
WINDOW_SECONDS = 3600     # 1 hour


def check_disk_growth_trend(metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Detect steady disk usage growth over time.
    """
    alerts = []

    disk = metrics.get("disk", {})
    root_usage = disk.get("root_percent")

    if root_usage is None:
        return alerts

    record_metric("disk_root_percent", root_usage)

    rate = calculate_rate("disk_root_percent", WINDOW_SECONDS)
    if rate is None:
        return alerts

    if rate >= CRITICAL_RATE:
        alerts.append({
            "source": "disk_growth_trend",
            "severity": "critical",
            "summary": "Disk usage increasing rapidly over time",
            "details": {
                "growth_rate_percent_per_sec": rate,
                "current_usage_percent": root_usage
            },
            "tags": ["disk", "trend", "growth"]
        })

    elif rate >= WARNING_RATE:
        alerts.append({
            "source": "disk_growth_trend",
            "severity": "warning",
            "summary": "Disk usage steadily increasing",
            "details": {
                "growth_rate_percent_per_sec": rate,
                "current_usage_percent": root_usage
            },
            "tags": ["disk", "trend", "growth"]
        })

    return alerts
