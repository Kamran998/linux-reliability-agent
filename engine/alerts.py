import json
import socket
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any, List

LOG_DIR = Path("logs")
ALERT_LOG = LOG_DIR / "alerts.log"


def _utc_now() -> str:

    return datetime.now(timezone.utc).isoformat()


def emit_alert(
    *,
    source: str,
    severity: str,
    summary: str,
    details: Optional[Dict[str, Any]] = None,
    tags: Optional[List[str]] = None,
    score: Optional[int] = None,
    mode: Optional[str] = None,
    incident_id: Optional[str] = None,
    event_type: str = "reliability_alert",
) -> None:
    """
    Emit a structured JSON alert to logs/alerts.log.

    This function must never raise an exception.
    """
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)

        alert = {
            "ts": _utc_now(),
            "host": socket.gethostname(),
            "source": source,
            "event_type": event_type,
            "severity": severity,
            "summary": summary,
            "details": details or {},
            "tags": tags or [],
            "score": score,
            "mode": mode,
            "incident_id": incident_id,
        }

        with ALERT_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(alert, sort_keys=True) + "\n")

    except Exception:
        # Fail silently: alerting must never crash the agent
        pass
