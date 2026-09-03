import json
import subprocess
import sys

def get_sheet_data(range_str):
    cmd = [
        "python3",
        "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py",
        "sheets", "get",
        "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k",
        range_str
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Error fetching range:", range_str, res.stderr, file=sys.stderr)
        return None
    return json.loads(res.stdout)

batch_size = 5000
start_row = 2
max_row = 23217

first_target = None
queue_count = 0

while start_row <= max_row:
    end_row = min(start_row + batch_size - 1, max_row)
    range_str = f"Блогпосты Сирейтс!A{start_row}:G{end_row}"
    data = get_sheet_data(range_str)
    if not data:
        break
    
    for idx, row in enumerate(data):
        current_sheet_row = start_row + idx
        row_padded = row + [""] * (6 - len(row))
        title_orig, url_orig, lang, status, title_navo, url_navo = row_padded[:6]
        
        if not url_orig or not url_orig.strip().startswith("http"):
            continue
        
        status_clean = status.strip()
        
        # In queue means status is "В очереди" or empty "" or status not in completed/error/in-progress
        # Wait, let me check what status values exist or if status is "" or "В очереди"
        if status_clean in ["В очереди", ""]:
            queue_count += 1
            if first_target is None:
                first_target = {
                    "row": current_sheet_row,
                    "title": title_orig,
                    "url": url_orig,
                    "lang": lang,
                    "status": status_clean
                }
    
    start_row = end_row + 1

print(json.dumps({
    "first_target": first_target,
    "total_queue_count": queue_count
}, indent=2, ensure_ascii=False))
