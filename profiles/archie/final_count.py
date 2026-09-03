import subprocess
import json
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
SCRIPT = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def count_remaining():
    batch_size = 5000
    start_row = 2
    end_total = 23217
    
    total_queued = 0
    total_done = 0
    total_in_progress = 0
    
    curr = start_row
    while curr <= end_total:
        batch_end = min(curr + batch_size - 1, end_total)
        rng_str = f"A{curr}:G{batch_end}"
        cmd = ["python3", SCRIPT, "sheets", "get", SHEET_ID, f"Блогпосты Сирейтс!{rng_str}"]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error reading {rng_str}: {res.stderr}")
            break
        rows = json.loads(res.stdout)
        
        for row in rows:
            col_b = row[1].strip() if len(row) > 1 and row[1] else ""
            col_d = row[3].strip() if len(row) > 3 and row[3] else ""
            
            if not col_b or not (col_b.startswith("http://") or col_b.startswith("https://")):
                continue
                
            if col_d.lower() in ["в очереди", "", "pending"]:
                total_queued += 1
            elif col_d.lower() in ["готово", "done"]:
                total_done += 1
            elif col_d.lower() in ["в процессе", "in progress"]:
                total_in_progress += 1
                
        curr = batch_end + 1
        
    print(f"Total queued: {total_queued}")
    print(f"Total done: {total_done}")
    print(f"Total in progress: {total_in_progress}")

if __name__ == "__main__":
    count_remaining()
