import subprocess
import json

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
CLI_PATH = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def fetch_batch(start_row, end_row):
    range_str = f"Блогпосты Сирейтс!A{start_row}:G{end_row}"
    cmd = [
        "python3", CLI_PATH, "sheets", "get",
        SHEET_ID, range_str
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return []
    try:
        data = json.loads(res.stdout)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and 'values' in data:
            return data['values']
        return []
    except Exception as e:
        return []

total_queued = 0
for start in range(2, 24000, 1000):
    end = start + 999
    rows = fetch_batch(start, end)
    if not rows:
        break
    for row in rows:
        link_orig = row[1] if len(row) > 1 else ""
        status = row[3] if len(row) > 3 else ""
        if not link_orig or not str(link_orig).startswith("http"):
            continue
        status_clean = str(status).strip().lower()
        if status_clean in ["в очереди", "", "in queue", "none"]:
            total_queued += 1

print(f"EXACT_REMAINING_QUEUE_COUNT={total_queued}")
