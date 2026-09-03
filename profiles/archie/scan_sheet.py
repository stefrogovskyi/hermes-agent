import subprocess
import json
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
CLI_PATH = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_range(rng):
    cmd = ["python3", CLI_PATH, "sheets", "get", SHEET_ID, rng]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching range {rng}: {res.stderr}")
        return None
    try:
        data = json.loads(res.stdout)
        if isinstance(data, dict):
            return data.get("values", [])
        elif isinstance(data, list):
            return data
        return []
    except Exception as e:
        print(f"Failed to parse JSON for range {rng}: {e}")
        return None

def main():
    chunks = [
        (2, 5001),
        (5002, 10001),
        (10002, 15001),
        (15002, 20001),
        (20002, 23217)
    ]
    
    found_row = None
    target_row_idx = None
    total_queued = 0
    total_valid_rows = 0
    
    for start, end in chunks:
        rng_str = f"Блогпосты Сирейтс!A{start}:G{end}"
        rows = get_range(rng_str)
        if not rows:
            print(f"No data returned for {rng_str}")
            continue
            
        for i, row in enumerate(rows):
            current_row_idx = start + i
            while len(row) < 6:
                row.append("")
                
            col_a, col_b, col_c, col_d, col_e, col_f = row[:6]
            col_b = col_b.strip()
            col_d = col_d.strip()
            
            if not col_b or not (col_b.startswith("http://") or col_b.startswith("https://")):
                continue
                
            total_valid_rows += 1
            
            is_queued = col_d == "" or col_d == "В очереди" or col_d is None
            if is_queued:
                total_queued += 1
                if found_row is None:
                    found_row = row
                    target_row_idx = current_row_idx

    print(f"RESULTS:")
    print(f"First queued row index: {target_row_idx}")
    print(f"First queued row data: {found_row}")
    print(f"Total queued count across sheet: {total_queued}")

if __name__ == "__main__":
    main()
