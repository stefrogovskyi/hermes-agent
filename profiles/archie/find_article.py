import json
import subprocess
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
GOOGLE_API = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

ranges = [
    "Блогпосты Сирейтс!A2:G5001",
    "Блогпосты Сирейтс!A5002:G10001",
    "Блогпосты Сирейтс!A10002:G15001",
    "Блогпосты Сирейтс!A15002:G20001",
    "Блогпосты Сирейтс!A20002:G23217"
]

all_rows = []
target_row = None
target_row_number = None

current_row_idx = 2  # Row 1 is header

for r in ranges:
    print(f"Fetching range {r}...")
    cmd = ["python3", GOOGLE_API, "sheets", "get", SHEET_ID, r]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching range {r}: {res.stderr}")
        continue
    try:
        data = json.loads(res.stdout)
    except Exception as e:
        print(f"Failed to parse json for {r}: {e}")
        continue
    
    # data can be list of rows or dict
    values = data.get("values", []) if isinstance(data, dict) else data
    if not isinstance(values, list):
        print(f"Unexpected data format: {type(values)}")
        continue
        
    for row in values:
        # row is a list of cells
        # A: title, B: link, C: lang, D: status, E: navo title, F: navo link
        title = row[0] if len(row) > 0 else ""
        link = row[1] if len(row) > 1 else ""
        lang = row[2] if len(row) > 2 else ""
        status = row[3] if len(row) > 3 else ""
        
        valid_link = bool(link and link.strip().startswith("http"))
        is_queued = status in ["В очереди", "", None] or status.strip() == ""
        
        all_rows.append({
            "row_num": current_row_idx,
            "title": title,
            "link": link,
            "lang": lang,
            "status": status,
            "valid_link": valid_link,
            "is_queued": is_queued
        })
        
        if target_row is None and is_queued and valid_link:
            target_row = {
                "row_num": current_row_idx,
                "title": title,
                "link": link,
                "lang": lang,
                "status": status
            }
            target_row_number = current_row_idx
            
        current_row_idx += 1

queued_count = sum(1 for r in all_rows if r["is_queued"] and r["valid_link"])

print(f"Total rows scanned: {len(all_rows)}")
print(f"Total queued rows remaining: {queued_count}")
if target_row:
    print(f"FOUND TARGET ROW: {target_row}")
else:
    print("NO QUEUED ARTICLE FOUND!")
