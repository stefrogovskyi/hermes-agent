import json
import subprocess
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB = "Блогпосты Сирейтс"
SCRIPT = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_sheet_range(rng):
    cmd = [sys.executable, SCRIPT, "sheets", "get", SHEET_ID, rng]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Error reading range:", rng, res.stderr)
        return None
    try:
        return json.loads(res.stdout)
    except Exception as e:
        print("Failed to parse JSON for range:", rng, e)
        return None

def update_cell(rng, values_matrix):
    cmd = [sys.executable, SCRIPT, "sheets", "update", SHEET_ID, rng, "--values", json.dumps(values_matrix)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Error updating range:", rng, res.stderr)
        return False
    return True

def main():
    batch_size = 5000
    start_row = 2
    max_row = 23217

    target_row = None
    target_data = None
    total_in_queue = 0

    print("Scanning sheet...")
    curr = start_row
    while curr <= max_row:
        end = min(curr + batch_size - 1, max_row)
        rng = f"{TAB}!A{curr}:G{end}"
        data = get_sheet_range(rng)
        
        if data is None or not isinstance(data, list):
            print(f"Could not read range A{curr}:G{end}")
            break

        values = data
        for i, row in enumerate(values):
            row_num = curr + i
            col_a = str(row[0]).strip() if len(row) > 0 and row[0] is not None else ""
            col_b = str(row[1]).strip() if len(row) > 1 and row[1] is not None else ""
            col_c = str(row[2]).strip() if len(row) > 2 and row[2] is not None else ""
            col_d = str(row[3]).strip() if len(row) > 3 and row[3] is not None else ""
            col_e = str(row[4]).strip() if len(row) > 4 and row[4] is not None else ""
            col_f = str(row[5]).strip() if len(row) > 5 and row[5] is not None else ""

            valid_url = col_b.startswith("http")
            status = col_d

            is_in_queue = valid_url and (status in ["В очереди", "", None] or status.lower() == "в очереди")
            
            if is_in_queue:
                total_in_queue += 1
                if target_row is None:
                    target_row = row_num
                    target_data = {
                        "row_num": row_num,
                        "title_orig": col_a,
                        "url_orig": col_b,
                        "lang": col_c if col_c else "English",
                        "status": status
                    }

        curr += batch_size

    print(f"Found target row: {target_row}")
    print(f"Target data: {target_data}")
    print(f"Total in queue: {total_in_queue}")

    if target_row:
        # Update status to "В процессе"
        update_rng = f"{TAB}!D{target_row}"
        success = update_cell(update_rng, [["В процессе"]])
        if success:
            print(f"Successfully updated row {target_row} status to 'В процессе'")
        else:
            print(f"Failed to update status for row {target_row}")

    with open("/tmp/target_article.json", "w") as f:
        json.dump({
            "target": target_data,
            "total_in_queue": total_in_queue
        }, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
