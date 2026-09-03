import subprocess
import json
import sys

python_bin = "python3"
script = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"
sheet_id = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
sheet_name = "Блогпосты Сирейтс"

batch_size = 5000
start_row = 2
end_row_max = 23217

all_rows = []
row_offset = start_row

target_row = None
target_data = None
total_queued = 0

print("Scanning sheet in batches...")

for b_start in range(2, 25000, batch_size):
    b_end = min(b_start + batch_size - 1, 23217)
    if b_start > 23217:
        break
    range_str = f"'{sheet_name}'!A{b_start}:G{b_end}"
    print(f"Fetching range {range_str}...")
    cmd = [python_bin, script, "sheets", "get", sheet_id, range_str]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching range {range_str}: {res.stderr}")
        sys.exit(1)
    
    rows = json.loads(res.stdout)
    if not rows:
        break
    
    for i, row in enumerate(rows):
        curr_row_num = b_start + i
        if curr_row_num > 23217:
            break
        
        # Extracted fields
        title_orig = row[0] if len(row) > 0 else ""
        link_orig = row[1] if len(row) > 1 else ""
        lang = row[2] if len(row) > 2 else ""
        status = row[3] if len(row) > 3 else ""
        
        # Skip empty/invalid rows (no link or trash)
        if not link_orig or not link_orig.startswith("http"):
            continue
        
        status_clean = status.strip()
        is_queued = status_clean in ["В очереди", ""] or not status
        
        if is_queued:
            total_queued += 1
            if target_row is None:
                target_row = curr_row_num
                target_data = {
                    "row_num": curr_row_num,
                    "title_orig": title_orig,
                    "link_orig": link_orig,
                    "lang": lang,
                    "status": status
                }

print(f"Target row found: {target_row}")
print(f"Target data: {target_data}")
print(f"Total queued items count: {total_queued}")

if target_row is not None:
    # Immediately update status to "В процессе"
    update_range = f"'{sheet_name}'!D{target_row}"
    cmd_up = [python_bin, script, "sheets", "update", "--values", '[["В процессе"]]', sheet_id, update_range]
    res_up = subprocess.run(cmd_up, capture_output=True, text=True)
    print("Update status output:", res_up.stdout, res_up.stderr)
    
    # Save target info to file for subsequent steps
    out = {
        "target": target_data,
        "total_queued_before_claim": total_queued,
        "total_queued_after_claim": total_queued - 1
    }
    with open("target_article.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
else:
    print("QUEUE_EMPTY")
