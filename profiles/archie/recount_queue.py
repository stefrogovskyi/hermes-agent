import subprocess
import json

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB = "Блогпосты Сирейтс"
API_SCRIPT = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_range(start_row, end_row):
    range_str = f"'{TAB}'!A{start_row}:F{end_row}"
    cmd = ["python3", API_SCRIPT, "sheets", "get", SHEET_ID, range_str]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return []
    try:
        data = json.loads(res.stdout)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get("values", [])
        return []
    except Exception:
        return []

batches = [(2, 5001), (5002, 10001), (10002, 15001), (15002, 20001), (20002, 23217)]

queue_count = 0

for start, end in batches:
    rows = get_range(start, end)
    for r in rows:
        url = r[1] if len(r) > 1 else ""
        status = r[3] if len(r) > 3 else ""
        
        if url.startswith("http://") or url.startswith("https://"):
            status_clean = status.strip()
            if status_clean in ["В очереди", ""]:
                queue_count += 1

print(f"REMAINING QUEUE COUNT: {queue_count}")
