import time
import argparse

from collector.sys_metrics import collect_sys_metrics
from engine.alerts import emit_alert

from checks.disk_pressure import check_disk_pressure
from checks.mem_pressure import check_memory_pressure
from checks.load_pressure import check_load_pressure
from checks.disk_growth_trend import check_disk_growth_trend
from engine.scoring import calculate_reliability
from checks.service_restarts import check_service_restarts
CHECKS = [
    check_disk_pressure,
    check_memory_pressure,
    check_load_pressure,
    check_disk_growth_trend,
    check_service_restarts,
]


def run(interval: int) -> None:
    """
    Main reliability monitoring loop.
    """
    while True:
        try:
            metrics = collect_sys_metrics()
            all_alerts = []

            for check in CHECKS:
                alerts = check(metrics)
                all_alerts.extend(alerts)

            score, mode = calculate_reliability(all_alerts)

            for alert in all_alerts:
                alert["score"] = score
                alert["mode"] = mode
                emit_alert(**alert)

        except Exception:
            pass

        time.sleep(interval)

def main() -> None:
    parser = argparse.ArgumentParser(description="Linux Reliability Agent")
    parser.add_argument(
        "--interval",
        type=int,
        default=10,
        help="Metric collection interval in seconds",
    )
    args = parser.parse_args()

    run(args.interval)


if __name__ == "__main__":
    main()
