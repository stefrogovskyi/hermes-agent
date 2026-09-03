import json
import subprocess
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
PYTHON_CLI = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_range(start_row, end_row):
    range_str = f"'{TAB_NAME}'!A{start_row}:G{end_row}"
    cmd = [sys.executable, PYTHON_CLI, "sheets", "get", SHEET_ID, range_str]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error reading range {range_str}: {res.stderr}", file=sys.stderr)
        return []
    try:
        data = json.loads(res.stdout)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get("values", [])
        return []
    except Exception as e:
        print(f"Error parsing json for {range_str}: {e}\nOutput: {res.stdout[:200]}", file=sys.stderr)
        return []

def main():
    start = 2
    step = 5000
    max_row = 23217
    
    target_row = None
    target_data = None
    queue_count = 0

    print("Scanning Google Sheet for queue status...")
    
    current_start = start
    while current_start <= max_row:
        current_end = min(current_start + step - 1, max_row)
        print(f"Fetching rows {current_start} to {current_end}...")
        rows = get_range(current_start, current_end)
        if not rows:
            print(f"No rows returned for {current_start}:{current_end}")
            break
        
        for idx, row in enumerate(rows):
            row_num = current_start + idx
            title = row[0].strip() if len(row) > 0 else ""
            url = row[1].strip() if len(row) > 1 else ""
            lang = row[2].strip() if len(row) > 2 else ""
            status = row[3].strip() if len(row) > 3 else ""

            # Check if row is garbage (no URL)
            if not url or not url.startswith("http"):
                continue

            # Check queue status: "В очереди", empty, or missing
            is_in_queue = status in ["", "В очереди"] or not status
            
            if is_in_queue:
                queue_count += 1
                if target_row is None:
                    target_row = row_num
                    target_data = {
                        "row_num": row_num,
                        "title": title,
                        "url": url,
                        "lang": lang,
                        "status": status
                    }

        current_start = current_end + 1

    print(f"\n--- SCAN RESULT ---")
    print(f"Target Row: {target_row}")
    print(f"Target Data: {target_data}")
    print(f"Total in Queue remaining: {queue_count}")

    with open("target_info.json", "w", encoding="utf-8") as f:
        json.dump({
            "target_row": target_row,
            "target_data": target_data,
            "queue_count": queue_count
        }, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
