import subprocess
import json
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
API_SCRIPT = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def run_cmd(cmd):
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {result.stderr}")
    return result.stdout

def get_rows_batch(start_row, end_row):
    range_str = f"Блогпосты Сирейтс!A{start_row}:G{end_row}"
    cmd = ["python3", API_SCRIPT, "sheets", "get", SHEET_ID, range_str]
    out = run_cmd(cmd)
    return json.loads(out)

def main():
    batch_size = 5000
    max_rows = 23217
    
    target_row_idx = None
    target_row_data = None
    
    queue_count = 0
    in_progress_count = 0
    done_count = 0
    error_count = 0
    empty_or_other_count = 0
    
    print("Scanning spreadsheet...")
    
    curr = 2
    while curr <= max_rows:
        end = min(curr + batch_size - 1, max_rows)
        print(f"Reading rows {curr} to {end}...")
        try:
            rows = get_rows_batch(curr, end)
        except Exception as e:
            print(f"Error reading batch {curr}-{end}: {e}")
            break
            
        if not rows:
            break
            
        for offset, row in enumerate(rows):
            actual_row = curr + offset
            
            # Helper to safely get column
            col_a = row[0].strip() if len(row) > 0 and row[0] else ""
            col_b = row[1].strip() if len(row) > 1 and row[1] else ""
            col_c = row[2].strip() if len(row) > 2 and row[2] else ""
            col_d = row[3].strip() if len(row) > 3 and row[3] else ""
            col_e = row[4].strip() if len(row) > 4 and row[4] else ""
            col_f = row[5].strip() if len(row) > 5 and row[5] else ""
            
            # Ignore empty or artifact rows without valid URL in col B
            if not col_b or not col_b.startswith("http"):
                empty_or_other_count += 1
                continue
                
            status = col_d
            
            if status == "Готово":
                done_count += 1
            elif status == "В процессе":
                in_progress_count += 1
            elif status == "Ошибка":
                error_count += 1
            elif status == "В очереди" or status == "":
                queue_count += 1
                if target_row_idx is None:
                    target_row_idx = actual_row
                    target_row_data = {
                        "row_num": actual_row,
                        "title_orig": col_a,
                        "url_orig": col_b,
                        "lang": col_c,
                        "status": col_d
                    }
            else:
                # Any other status treat as queue if not done/error/in_progress? Prompt says: "со статусом в колонке D равным 'В очереди', пустым, или отсутствующим"
                pass
                
        curr = end + 1

    print("\n--- Queue Summary ---")
    print(f"Target Row: {target_row_idx}")
    print(f"Target Article: {target_row_data}")
    print(f"Total in Queue: {queue_count}")
    print(f"In Progress: {in_progress_count}")
    print(f"Done: {done_count}")
    print(f"Errors: {error_count}")
    print(f"Empty/Artifacts: {empty_or_other_count}")

    if target_row_data:
        # Save target article info to json for script processing
        with open("claimed_article.json", "w") as f:
            json.dump({
                "target": target_row_data,
                "queue_count": queue_count,
                "done_count": done_count,
                "in_progress_count": in_progress_count,
                "error_count": error_count
            }, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
