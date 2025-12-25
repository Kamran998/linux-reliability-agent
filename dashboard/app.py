from flask import Flask, render_template
import json
from pathlib import Path

app = Flask(__name__)

LOG_DIR = Path("../logs")
STATE_DIR = Path("../state")


def load_json(path):
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def load_jsonl(path, limit=50):
    if not path.exists():
        return []
    lines = path.read_text().splitlines()
    entries = []
    for line in lines[-limit:]:
        try:
            entries.append(json.loads(line))
        except Exception:
            continue
    return entries


@app.route("/")
def index():
    health = load_json(LOG_DIR / "health.json")
    alerts = load_jsonl(LOG_DIR / "alerts.log", limit=50)
    incidents = load_jsonl(LOG_DIR / "incidents.log", limit=10)

    return render_template(
        "index.html",
        health=health,
        alerts=alerts,
        incidents=incidents,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
