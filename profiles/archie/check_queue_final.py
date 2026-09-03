import subprocess
import json

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
SCRIPT_PATH = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_range(start_row, end_row):
    range_str = f"'{TAB_NAME}'!A{start_row}:G{end_row}"
    cmd = ["python3", SCRIPT_PATH, "sheets", "get", SHEET_ID, range_str]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return None
    try:
        return json.loads(res.stdout)
    except:
        return None

def main():
    batch_size = 3000
    total_rows = 23217
    in_queue_count = 0
    done_count = 0
    
    current_row = 2
    while current_row <= total_rows:
        end_row = min(current_row + batch_size - 1, total_rows)
        rows = get_range(current_row, end_row)
        if rows:
            for r in rows:
                col_b = r[1] if len(r) > 1 else ""
                col_d = r[3] if len(r) > 3 else ""
                if col_b and col_b.startswith("http"):
                    status = col_d.strip()
                    if status in ["В очереди", ""] or not status:
                        in_queue_count += 1
                    elif status == "Готово":
                        done_count += 1
        current_row += batch_size
        
    print(f"Remaining in queue: {in_queue_count}")
    print(f"Total done: {done_count}")

if __name__ == "__main__":
    main()
