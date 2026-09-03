import subprocess
import json
import sys

SCRIPT_PATH = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"
SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"

def get_range(range_str):
    cmd = ["python3", SCRIPT_PATH, "sheets", "get", SHEET_ID, range_str]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        print(f"Error reading {range_str}: {res.stderr}")
        return None
    try:
        return json.loads(res.stdout)
    except Exception as e:
        print(f"JSON parse error for {range_str}: {e}")
        return None

def main():
    chunk_size = 1000
    total_rows = 23217
    start_row = 2
    
    queued_row_idx = None
    queued_row_data = None
    
    total_queued_count = 0
    total_valid_rows = 0
    
    current_start = start_row
    while current_start <= total_rows:
        current_end = min(current_start + chunk_size - 1, total_rows)
        range_str = f"'{TAB_NAME}'!A{current_start}:G{current_end}"
        data = get_range(range_str)
        if not data or not isinstance(data, list):
            print(f"No valid data returned for {range_str}")
            current_start += chunk_size
            continue
            
        for offset, row in enumerate(data):
            row_num = current_start + offset
            # A=Title, B=URL, C=Language, D=Status, E=Navo Title, F=Navo Link
            url = row[1].strip() if len(row) > 1 and row[1] else ""
            status = row[3].strip() if len(row) > 3 and row[3] else ""
            
            # Skip empty URL or junk
            if not url or not url.startswith("http"):
                continue
                
            total_valid_rows += 1
            
            if status in ["В очереди", "", None]:
                total_queued_count += 1
                if queued_row_idx is None:
                    queued_row_idx = row_num
                    queued_row_data = row
                    
        print(f"Scanned up to row {current_end}... (Found queued so far: {total_queued_count})")
        current_start += chunk_size
        
    print(f"Done scanning.")
    print(f"First queued row: {queued_row_idx}")
    print(f"First queued data: {queued_row_data}")
    print(f"Total valid rows: {total_valid_rows}")
    print(f"Total queued count across sheet: {total_queued_count}")

if __name__ == "__main__":
    main()
