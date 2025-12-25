import json
import socket
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


HEALTH_FILE = Path("logs/health.json")
STATE_INCIDENTS = Path("state/incidents.json")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _count_active_incidents() -> int:
    if not STATE_INCIDENTS.exists():
        return 0
    try:
        with STATE_INCIDENTS.open("r", encoding="utf-8") as f:
            incidents = json.load(f)
        return len(incidents)
    except Exception:
        return 0


def write_health_snapshot(
    *,
    score: int,
    mode: str,
    active_alerts: int,
) -> None:
    """
    Write current system health snapshot.
    Must never raise.
    """
    try:
        HEALTH_FILE.parent.mkdir(parents=True, exist_ok=True)

        snapshot = {
            "ts": _utc_now(),
            "host": socket.gethostname(),
            "score": score,
            "mode": mode,
            "active_alerts": active_alerts,
            "active_incidents": _count_active_incidents(),
        }

        with HEALTH_FILE.open("w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2)

    except Exception:
        pass
