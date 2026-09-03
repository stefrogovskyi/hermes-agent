import json
import subprocess

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
SCRIPT = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_sheet_range(rng):
    cmd = ["python3", SCRIPT, "sheets", "get", SHEET_ID, f"{TAB_NAME}!{rng}"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return None
    try:
        data = json.loads(res.stdout)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get("values", [])
        return []
    except Exception as e:
        return None

def main():
    start_row = 2
    batch_size = 5000
    max_row = 23217

    remaining_count = 0
    total_valid = 0

    current = start_row
    while current <= max_row:
        end = min(current + batch_size - 1, max_row)
        rng_str = f"A{current}:G{end}"
        rows = get_sheet_range(rng_str)
        if not rows:
            break
        
        for idx, row in enumerate(rows):
            col_b = row[1].strip() if len(row) > 1 else ""
            col_d = row[3].strip() if len(row) > 3 else ""

            if not col_b or not col_b.startswith("http"):
                continue

            total_valid += 1

            if col_d.lower() in ["в очереди", ""] or not col_d:
                remaining_count += 1
        
        current = end + 1

    print(f"Remaining in queue: {remaining_count}")
    print(f"Total valid articles: {total_valid}")

if __name__ == "__main__":
    main()
