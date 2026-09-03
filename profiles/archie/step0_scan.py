import subprocess
import json
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
CLI_PATH = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_range(range_str):
    cmd = [
        "python3", CLI_PATH, "sheets", "get", SHEET_ID, f'"{TAB_NAME}"!{range_str}'
    ]
    res = subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching range {range_str}: {res.stderr}")
        return None
    try:
        data = json.loads(res.stdout)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get("values", [])
        return []
    except Exception as e:
        print(f"JSON decode error: {e}, stdout: {res.stdout[:200]}")
        return None

def update_cell(cell_ref, value):
    cmd = [
        "python3", CLI_PATH, "sheets", "update",
        "--values", json.dumps([[value]]),
        SHEET_ID, f'"{TAB_NAME}"!{cell_ref}'
    ]
    res = subprocess.run(" ".join(cmd), shell=True, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error updating cell {cell_ref}: {res.stderr}")
        return False
    print(f"Successfully updated {cell_ref} to {value}")
    return True

print("Step 0: Scanning sheet for first eligible row...")
found_row = None
queue_count = 0

batch_size = 5000
end_row_total = 23217

for batch_start in range(2, end_row_total + 1, batch_size):
    batch_end = min(batch_start + batch_size - 1, end_row_total)
    range_str = f"A{batch_start}:G{batch_end}"
    print(f"Fetching range {range_str}...")
    rows = get_range(range_str)
    if not rows:
        print(f"No rows returned for {range_str}")
        continue
    
    for i, row in enumerate(rows):
        actual_row_num = batch_start + i
        col_a = row[0] if len(row) > 0 else ""
        col_b = row[1] if len(row) > 1 else ""
        col_c = row[2] if len(row) > 2 else ""
        col_d = row[3] if len(row) > 3 else ""
        col_e = row[4] if len(row) > 4 else ""
        col_f = row[5] if len(row) > 5 else ""

        # Check validity
        if not col_b.strip() or not col_b.startswith("http"):
            continue # Skip invalid/garbage rows
        
        status = col_d.strip()
        is_in_queue = (status == "В очереди" or status == "" or status is None)
        
        if is_in_queue:
            queue_count += 1
            if found_row is None:
                found_row = {
                    "row_num": actual_row_num,
                    "title_orig": col_a,
                    "url_orig": col_b,
                    "lang": col_c,
                    "status": col_d
                }

print(f"\nScan complete. Total items in queue: {queue_count}")
if found_row:
    print(f"First target row found at row {found_row['row_num']}:")
    print(json.dumps(found_row, ensure_ascii=False, indent=2))
    # Update status to "В процессе"
    update_cell(f"D{found_row['row_num']}", "В процессе")
    with open('/opt/hermes/profiles/archie/target_row.json', 'w', encoding='utf-8') as f:
        found_row['total_remaining_in_queue'] = queue_count
        json.dump(found_row, f, ensure_ascii=False, indent=2)
else:
    print("Queue is empty. All articles processed.")
