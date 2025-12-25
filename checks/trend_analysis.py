import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

STATE_DIR = Path("state")
MAX_POINTS = 360  # e.g. 1 hour @ 10s interval


def _load_history(name: str) -> List[Dict[str, Any]]:
    path = STATE_DIR / f"{name}.json"
    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_history(name: str, history: List[Dict[str, Any]]) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    path = STATE_DIR / f"{name}.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(history[-MAX_POINTS:], f)


def record_metric(name: str, value: float) -> None:
    """
    Record a metric value with timestamp.
    """
    history = _load_history(name)
    history.append({
        "ts": int(time.time()),
        "value": value
    })
    _save_history(name, history)


def calculate_rate(name: str, window_seconds: int) -> Optional[float]:
    """
    Calculate rate of change over a time window.
    Returns units per second.
    """
    history = _load_history(name)
    if len(history) < 2:
        return None

    now = int(time.time())
    window = [p for p in history if p["ts"] >= now - window_seconds]

    if len(window) < 2:
        return None

    start = window[0]
    end = window[-1]

    delta_value = end["value"] - start["value"]
    delta_time = end["ts"] - start["ts"]

    if delta_time <= 0:
        return None

    return round(delta_value / delta_time, 4)
