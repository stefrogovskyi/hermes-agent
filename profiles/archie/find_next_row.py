import subprocess
import json
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB = "Блогпосты Сирейтс"
SCRIPT = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_range(start_row, end_row):
    range_str = f"'{TAB}'!A{start_row}:G{end_row}"
    cmd = ["python3", SCRIPT, "sheets", "get", SHEET_ID, range_str]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error reading range {range_str}: {res.stderr}")
        return None
    try:
        data = json.loads(res.stdout)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get("values", [])
        return []
    except Exception as e:
        print(f"JSON parse error: {e}, stdout: {res.stdout[:200]}")
        return None

def main():
    start = 2
    step = 5000
    max_row = 23217
    
    first_target_row = None
    target_data = None
    
    in_queue_count = 0
    total_valid = 0
    
    current_start = start
    while current_start <= max_row:
        current_end = min(current_start + step - 1, max_row)
        print(f"Fetching rows {current_start} to {current_end}...")
        rows = get_range(current_start, current_end)
        if not rows:
            print("No rows returned or error.")
            break
        
        for idx, row in enumerate(rows):
            actual_row_num = current_start + idx
            col_a = row[0] if len(row) > 0 else ""
            col_b = row[1] if len(row) > 1 else ""
            col_c = row[2] if len(row) > 2 else ""
            col_d = row[3] if len(row) > 3 else ""
            
            # Skip invalid/garbage rows without link in col B
            if not col_b or not col_b.strip().startswith("http"):
                continue
            
            total_valid += 1
            
            status = col_d.strip()
            if status in ["В очереди", "В очереди\n", "", None] or not status:
                in_queue_count += 1
                if first_target_row is None:
                    first_target_row = actual_row_num
                    target_data = {
                        "row_num": actual_row_num,
                        "title_orig": col_a,
                        "link_orig": col_b,
                        "lang": col_c,
                        "status": status
                    }
        
        current_start = current_end + 1

    print("--- RESULTS ---")
    print(f"Total valid articles seen: {total_valid}")
    print(f"Total in queue: {in_queue_count}")
    if target_data:
        print(f"First row to process: {json.dumps(target_data, ensure_ascii=False)}")
    else:
        print("No articles in queue!")

if __name__ == "__main__":
    main()
