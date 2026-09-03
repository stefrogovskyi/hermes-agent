import json
import subprocess
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
PYTHON_CLI = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_range(start_row, end_row):
    range_str = f"'{TAB_NAME}'!A{start_row}:G{end_row}"
    cmd = [
        "python3", PYTHON_CLI, "sheets", "get", SHEET_ID, range_str
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching range {range_str}: {res.stderr}")
        return []
    try:
        return json.loads(res.stdout)
    except Exception as e:
        print(f"Failed to parse JSON for {range_str}: {e}")
        return []

def main():
    chunk_size = 5000
    start = 2
    total_max = 23217
    
    first_pending_row = None
    first_pending_data = None
    remaining_count = 0
    
    while start <= total_max:
        end = min(start + chunk_size - 1, total_max)
        print(f"Fetching rows A{start}:G{end}...")
        rows = get_range(start, end)
        if not rows:
            print(f"No data returned for range {start}:{end}")
            break
        
        for idx, row in enumerate(rows):
            current_row_num = start + idx
            title = row[0].strip() if len(row) > 0 and row[0] else ""
            link = row[1].strip() if len(row) > 1 and row[1] else ""
            lang = row[2].strip() if len(row) > 2 and row[2] else "English"
            status = row[3].strip() if len(row) > 3 and row[3] else ""
            
            # Check if row is valid (must have valid link starting with http)
            if not link.startswith("http"):
                continue
            
            # Check pending status
            if status in ["В очереди", "", None]:
                remaining_count += 1
                if first_pending_row is None:
                    first_pending_row = current_row_num
                    first_pending_data = {
                        "row_num": current_row_num,
                        "title": title,
                        "link": link,
                        "lang": lang,
                        "status": status
                    }
        
        start = end + 1

    if first_pending_row is None:
        print("QUEUE_EMPTY")
        sys.exit(0)

    print(f"Found first pending row: {first_pending_data}")
    print(f"Total remaining in queue: {remaining_count}")

    # Lock row: Update status to "В процессе"
    lock_range = f"'{TAB_NAME}'!D{first_pending_row}"
    update_cmd = [
        "python3", PYTHON_CLI, "sheets", "update", "--values", json.dumps([["В процессе"]]), SHEET_ID, lock_range
    ]
    res_update = subprocess.run(update_cmd, capture_output=True, text=True)
    print(f"Lock result stdout: {res_update.stdout}")
    print(f"Lock result stderr: {res_update.stderr}")

    # Output JSON result for caller
    result = {
        "pending_item": first_pending_data,
        "total_remaining": remaining_count
    }
    with open("locked_article.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
