import json
from pathlib import Path
FB_FILE = Path("./feedback.json")
if not FB_FILE.exists():
    FB_FILE.write_text("[]")

def store_feedback(entry: dict):
    data = json.loads(FB_FILE.read_text())
    data.append(entry)
    FB_FILE.write_text(json.dumps(data, indent=2))
