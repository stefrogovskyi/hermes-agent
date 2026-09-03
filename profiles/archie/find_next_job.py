import json
import subprocess
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB = "Блогпосты Сирейтс"

def get_range(start_row, end_row):
    range_str = f"'{TAB}'!A{start_row}:F{end_row}"
    cmd = [
        "python3", "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py",
        "sheets", "get", SHEET_ID, range_str
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching {range_str}: {res.stderr}", file=sys.stderr)
        return []
    try:
        return json.loads(res.stdout)
    except Exception as e:
        print(f"JSON decode error: {e}", file=sys.stderr)
        return []

batch_size = 5000
total_rows = 23217

target_row = None
target_data = None
total_in_queue = 0

for start in range(2, total_rows + 1, batch_size):
    end = min(start + batch_size - 1, total_rows)
    print(f"Scanning rows {start} to {end}...")
    rows = get_range(start, end)
    for idx, row in enumerate(rows):
        row_num = start + idx
        # Ensure row has enough elements
        title = row[0] if len(row) > 0 else ""
        link = row[1] if len(row) > 1 else ""
        lang = row[2] if len(row) > 2 else ""
        status = row[3] if len(row) > 3 else ""
        
        # Check if link is valid
        if not link or not link.startswith("http"):
            continue
            
        status_clean = status.strip().lower() if status else ""
        if status_clean in ["в очереди", "", "in queue"]:
            total_in_queue += 1
            if target_row is None:
                target_row = row_num
                target_data = {
                    "row_num": row_num,
                    "orig_title": title,
                    "orig_link": link,
                    "lang": lang,
                    "status": status
                }

print(f"Target row found: {target_row}")
print(f"Target data: {target_data}")
print(f"Total remaining in queue across table: {total_in_queue}")

