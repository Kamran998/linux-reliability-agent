import time
import argparse

from collector.sys_metrics import collect_sys_metrics
from engine.alerts import emit_alert

from checks.disk_pressure import check_disk_pressure
from checks.mem_pressure import check_memory_pressure
from checks.load_pressure import check_load_pressure
from checks.disk_growth_trend import check_disk_growth_trend


CHECKS = [
    check_disk_pressure,
    check_memory_pressure,
    check_load_pressure,
    check_disk_growth_trend,
]


def run(interval: int) -> None:
    """
    Main reliability monitoring loop.
    """
    while True:
        try:
            metrics = collect_sys_metrics()

            for check in CHECKS:
                alerts = check(metrics)
                for alert in alerts:
                    emit_alert(**alert)

        except Exception:
            # Never let the agent crash
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
