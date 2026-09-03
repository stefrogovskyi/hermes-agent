import subprocess
import json
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
CLI_PATH = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_rows(range_name):
    cmd = ["python3", CLI_PATH, "sheets", "get", SHEET_ID, range_name]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching range {range_name}: {res.stderr}")
        return None
    try:
        return json.loads(res.stdout)
    except Exception as e:
        print(f"JSON decode error: {e}, output={res.stdout[:200]}")
        return None

batch_size = 3000
start_row = 2
max_row = 23217

first_queue_item = None
total_queue_count = 0

print("Scanning sheet for queue items...")

row_cursor = start_row
while row_cursor <= max_row:
    end_row = min(row_cursor + batch_size - 1, max_row)
    range_str = f"'Блогпосты Сирейтс'!A{row_cursor}:G{end_row}"
    print(f"Fetching range A{row_cursor}:G{end_row}...")
    data = get_rows(range_str)
    if not data:
        print(f"Failed to fetch data batch starting at {row_cursor}.")
        row_cursor += batch_size
        continue
    
    for i, row in enumerate(data):
        current_row_idx = row_cursor + i
        col_a = row[0].strip() if len(row) > 0 else ""
        col_b = row[1].strip() if len(row) > 1 else ""
        col_c = row[2].strip() if len(row) > 2 else ""
        col_d = row[3].strip() if len(row) > 3 else ""
        
        # Valid URL check
        if not col_b.startswith("http"):
            continue
        
        status_norm = col_d.strip()
        if status_norm in ["В очереди", "", "v ocheredi", "in queue"]:
            total_queue_count += 1
            if first_queue_item is None:
                first_queue_item = {
                    "row_index": current_row_idx,
                    "title": col_a,
                    "url": col_b,
                    "lang": col_c,
                    "status": col_d
                }

    row_cursor += batch_size

print(f"\n--- SCAN COMPLETE ---")
print(f"Total articles in queue across all rows: {total_queue_count}")

if first_queue_item:
    print(f"\nFirst Queue Item Selected:")
    print(json.dumps(first_queue_item, indent=2, ensure_ascii=False))
    
    # Save selection info to file
    with open("/opt/hermes/profiles/archie/current_item.json", "w", encoding="utf-8") as f:
        json.dump({"item": first_queue_item, "total_queue": total_queue_count}, f, ensure_ascii=False, indent=2)

    # Update status immediately to "В процессе"
    update_range = f"'Блогпосты Сирейтс'!D{first_queue_item['row_index']}"
    update_cmd = ["python3", CLI_PATH, "sheets", "update", SHEET_ID, update_range, "--values", '[["В процессе"]]']
    up_res = subprocess.run(update_cmd, capture_output=True, text=True)
    print("Update status response:")
    print(up_res.stdout)
    if up_res.returncode != 0:
        print("Update error:", up_res.stderr)
else:
    print("No items found in queue.")

