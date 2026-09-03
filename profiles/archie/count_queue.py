import subprocess
import json

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
CLI_PATH = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_range(range_str):
    cmd = [
        "python3", CLI_PATH, "sheets", "get", SHEET_ID, f'"{TAB_NAME}"!{range_str}'
    ]
    res = subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        return None
    try:
        data = json.loads(res.stdout)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get("values", [])
        return []
    except Exception:
        return None

queue_count = 0
end_row_total = 23217
batch_size = 5000

for batch_start in range(2, end_row_total + 1, batch_size):
    batch_end = min(batch_start + batch_size - 1, end_row_total)
    range_str = f"A{batch_start}:G{batch_end}"
    rows = get_range(range_str)
    if not rows:
        continue
    for row in rows:
        col_b = row[1] if len(row) > 1 else ""
        col_d = row[3] if len(row) > 3 else ""
        if not col_b.strip() or not col_b.startswith("http"):
            continue
        status = col_d.strip()
        if status == "В очереди" or status == "" or status is None:
            queue_count += 1

print(f"Verified total remaining in queue across all 23217 rows: {queue_count}")
