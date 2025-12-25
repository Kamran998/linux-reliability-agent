import json
import time
import uuid
from pathlib import Path
from typing import List, Dict, Any, Optional

STATE_FILE = Path("state/incidents.json")
INCIDENT_LOG = Path("logs/incidents.log")
WINDOW_SECONDS = 300  # 5 minutes


def _load_incidents() -> List[Dict[str, Any]]:
    if not STATE_FILE.exists():
        return []
    try:
        with STATE_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_incidents(incidents: List[Dict[str, Any]]) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with STATE_FILE.open("w", encoding="utf-8") as f:
        json.dump(incidents[-20:], f)


def _infer_root_cause(alerts: List[Dict[str, Any]]) -> str:
    sources = {a.get("source") for a in alerts}

    if "disk_growth_trend" in sources or "disk_pressure" in sources:
        return "disk_exhaustion"
    if "mem_pressure" in sources and "load_pressure" in sources:
        return "memory_pressure"
    if "service_restarts" in sources:
        return "service_instability"
    if len(sources) > 1:
        return "resource_exhaustion"

    return "unknown"


def correlate_incident(alerts: List[Dict[str, Any]]) -> Optional[str]:
    """
    Attach alerts to an incident if conditions are met.
    Returns incident_id or None.
    """
    if not alerts:
        return None

    now = int(time.time())
    incidents = _load_incidents()

    # Try to attach to existing incident
    for incident in incidents:
        if now - incident["last_seen"] <= WINDOW_SECONDS:
            incident["alerts"].extend(alerts)
            incident["last_seen"] = now
            incident["root_cause"] = _infer_root_cause(incident["alerts"])
            _save_incidents(incidents)
            return incident["id"]

    # Create new incident
    if len(alerts) >= 2 or any(a["severity"] == "critical" for a in alerts):
        incident_id = str(uuid.uuid4())
        incident = {
            "id": incident_id,
            "created": now,
            "last_seen": now,
            "root_cause": _infer_root_cause(alerts),
            "alerts": alerts,
        }
        incidents.append(incident)
        _save_incidents(incidents)

        INCIDENT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with INCIDENT_LOG.open("a", encoding="utf-8") as f:
            f.write(json.dumps(incident) + "\n")

        return incident_id

    return None
