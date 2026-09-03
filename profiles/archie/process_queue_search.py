import subprocess
import json
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
SCRIPT = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_range(rng):
    cmd = ["python3", SCRIPT, "sheets", "get", SHEET_ID, rng]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching range {rng}: {res.stderr}", file=sys.stderr)
        return None
    try:
        data = json.loads(res.stdout)
        return data
    except Exception as e:
        print(f"Error parsing JSON for {rng}: {e}", file=sys.stderr)
        return None

ranges = [
    ("Блогпосты Сирейтс!A2:G5001", 2),
    ("Блогпосты Сирейтс!A5002:G10001", 5002),
    ("Блогпосты Сирейтс!A10002:G15001", 10002),
    ("Блогпосты Сирейтс!A15002:G20001", 15002),
    ("Блогпосты Сирейтс!A20002:G23217", 20002)
]

first_eligible_row = None
first_eligible_data = None
total_queue_count = 0

for rng, start_row in ranges:
    print(f"Fetching {rng}...")
    data = get_range(rng)
    if not data:
        continue
    
    if isinstance(data, dict):
        rows = data.get("values", [])
    elif isinstance(data, list):
        rows = data
    else:
        rows = []

    for idx, row in enumerate(rows):
        row_num = start_row + idx
        # Columns: A=0, B=1, C=2, D=3, E=4, F=5
        orig_title = row[0] if len(row) > 0 else ""
        orig_url = row[1] if len(row) > 1 else ""
        lang = row[2] if len(row) > 2 else ""
        status = row[3] if len(row) > 3 else ""
        
        orig_url_str = str(orig_url).strip()
        if not (orig_url_str.startswith("http://") or orig_url_str.startswith("https://")):
            continue
            
        status_str = str(status).strip()
        if status_str in ["", "В очереди"] or not status_str:
            total_queue_count += 1
            if first_eligible_row is None:
                first_eligible_row = row_num
                first_eligible_data = {
                    "row_num": row_num,
                    "title": orig_title,
                    "url": orig_url_str,
                    "lang": lang,
                    "status": status_str
                }

print(f"TOTAL_QUEUE_COUNT: {total_queue_count}")
print(f"FIRST_ELIGIBLE_DATA: {json.dumps(first_eligible_data, ensure_ascii=False)}")
