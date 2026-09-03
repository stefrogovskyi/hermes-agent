import subprocess
import json

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
SCRIPT_PATH = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

chunks = [
    (2, 5001),
    (5002, 10001),
    (10002, 15001),
    (15002, 20001),
    (20002, 23217)
]

total_in_queue = 0

for start_r, end_r in chunks:
    range_str = f"'{TAB_NAME}'!A{start_r}:G{end_r}"
    cmd = ["python3", SCRIPT_PATH, "sheets", "get", SHEET_ID, range_str]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        continue
    try:
        rows = json.loads(res.stdout)
        for row in rows:
            if not row or len(row) < 2:
                continue
            orig_url = row[1].strip() if len(row) > 1 else ""
            status = row[3].strip() if len(row) > 3 else ""
            if orig_url.startswith("http") and status in ["В очереди", ""]:
                total_in_queue += 1
    except Exception as e:
        print("Error:", e)

print(f"REMAINING IN QUEUE (EXACT): {total_in_queue}")
