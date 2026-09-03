import json
import subprocess

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
        return []
    try:
        return json.loads(res.stdout)
    except Exception:
        return []

def main():
    chunk_size = 5000
    start = 2
    total_max = 23217
    remaining_count = 0
    
    while start <= total_max:
        end = min(start + chunk_size - 1, total_max)
        rows = get_range(start, end)
        if not rows:
            break
        
        for row in rows:
            link = row[1].strip() if len(row) > 1 and row[1] else ""
            status = row[3].strip() if len(row) > 3 and row[3] else ""
            
            if not link.startswith("http"):
                continue
            
            if status in ["В очереди", "", None]:
                remaining_count += 1
                
        start = end + 1

    print(f"EXACT_REMAINING_IN_QUEUE: {remaining_count}")

if __name__ == "__main__":
    main()
