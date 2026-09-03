import json
import subprocess
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB = "Блогпосты Сирейтс"
API_SCRIPT = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_range(start_row, end_row):
    range_str = f"'{TAB}'!A{start_row}:G{end_row}"
    cmd = ["python3", API_SCRIPT, "sheets", "get", SHEET_ID, range_str]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error reading range {range_str}: {res.stderr}", file=sys.stderr)
        return []
    try:
        data = json.loads(res.stdout)
        return data
    except Exception as e:
        print(f"JSON decode error: {e}", file=sys.stderr)
        return []

def main():
    total_rows = 23217
    batch_size = 5000
    
    first_target_row = None
    target_data = None
    queue_count = 0

    curr_row = 2
    while curr_row <= total_rows:
        end_row = min(curr_row + batch_size - 1, total_rows)
        print(f"Fetching rows {curr_row} to {end_row}...")
        rows = get_range(curr_row, end_row)
        
        for idx, row in enumerate(rows):
            row_num = curr_row + idx
            
            # Check length of row
            col_a = row[0] if len(row) > 0 else ""
            col_b = row[1] if len(row) > 1 else ""
            col_c = row[2] if len(row) > 2 else ""
            col_d = row[3] if len(row) > 3 else ""
            
            # Valid link check
            if not col_b or not isinstance(col_b, str) or not col_b.startswith("http"):
                continue
                
            status = col_d.strip() if col_d else ""
            
            # Check if in queue
            is_queue = status == "" or status == "В очереди" or status is None
            
            if is_queue:
                queue_count += 1
                if first_target_row is None:
                    first_target_row = row_num
                    target_data = {
                        "row": row_num,
                        "title_orig": col_a,
                        "url_orig": col_b,
                        "lang": col_c if col_c else "English",
                        "status": status
                    }
        
        curr_row = end_row + 1

    print(f"Total in queue: {queue_count}")
    if first_target_row:
        print(f"Target row found: {first_target_row}")
        print(json.dumps(target_data, ensure_ascii=False, indent=2))
        
        # Update status to "В процессе"
        update_range = f"'{TAB}'!D{first_target_row}"
        update_cmd = ["python3", API_SCRIPT, "sheets", "update", SHEET_ID, update_range, "В процессе"]
        res = subprocess.run(update_cmd, capture_output=True, text=True)
        print("Update response:", res.stdout)
    else:
        print("No target row found in entire queue.")

if __name__ == "__main__":
    main()
