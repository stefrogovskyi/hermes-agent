import subprocess
import json
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
SCRIPT = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_sheet_range(rng):
    cmd = ["python3", SCRIPT, "sheets", "get", SHEET_ID, f"Блогпосты Сирейтс!{rng}"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching range {rng}: {res.stderr}", file=sys.stderr)
        return None
    try:
        return json.loads(res.stdout)
    except Exception as e:
        print(f"JSON decode error for {rng}: {e}", file=sys.stderr)
        return None

def main():
    batch_size = 5000
    start_row = 2
    end_total = 23217
    
    first_pending_row = None
    first_pending_data = None
    
    total_queued = 0
    total_valid_rows = 0
    
    curr = start_row
    while curr <= end_total:
        batch_end = min(curr + batch_size - 1, end_total)
        rng_str = f"A{curr}:G{batch_end}"
        print(f"Fetching range {rng_str}...")
        rows = get_sheet_range(rng_str)
        if not rows:
            print(f"Failed to fetch {rng_str}")
            break
        
        for i, row in enumerate(rows):
            actual_row = curr + i
            # Check length of row
            col_a = row[0].strip() if len(row) > 0 and row[0] else ""
            col_b = row[1].strip() if len(row) > 1 and row[1] else ""
            col_c = row[2].strip() if len(row) > 2 and row[2] else ""
            col_d = row[3].strip() if len(row) > 3 and row[3] else ""
            
            # Skip invalid/empty URL rows
            if not col_b or not (col_b.startswith("http://") or col_b.startswith("https://")):
                continue
            
            total_valid_rows += 1
            
            is_pending = col_d.lower() in ["в очереди", "", "v ocheredi", "pending"] or col_d == ""
            if is_pending:
                total_queued += 1
                if first_pending_row is None:
                    first_pending_row = actual_row
                    first_pending_data = {
                        "row": actual_row,
                        "title_orig": col_a,
                        "url_orig": col_b,
                        "lang": col_c or "English",
                        "status": col_d
                    }
        
        curr = batch_end + 1
        
    print(f"\n--- SCAN RESULTS ---")
    print(f"Total valid articles in sheet: {total_valid_rows}")
    print(f"Total remaining in queue ('В очереди'/empty): {total_queued}")
    print(f"First pending article: {first_pending_data}")

if __name__ == "__main__":
    main()
