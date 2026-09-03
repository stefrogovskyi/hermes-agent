import subprocess
import json
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
SCRIPT = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_range(rng):
    cmd = ["python3", SCRIPT, "sheets", "get", SHEET_ID, f"{TAB_NAME}!{rng}"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching range {rng}: {res.stderr}")
        return None
    try:
        data = json.loads(res.stdout)
        return data
    except Exception as e:
        print(f"Failed to parse json for {rng}: {e}")
        return None

def main():
    ranges = [
        ("A2:G5001", 2),
        ("A5002:G10001", 5002),
        ("A10002:G15001", 10002),
        ("A15002:G20001", 15002),
        ("A20002:G23217", 20002)
    ]
    
    first_target = None
    total_queued = 0
    total_valid_rows = 0
    
    for rng_str, start_row in ranges:
        print(f"Fetching {rng_str}...")
        data = get_range(rng_str)
        if not data:
            continue
        
        if isinstance(data, dict):
            rows = data.get("values", [])
        elif isinstance(data, list):
            rows = data
        else:
            rows = []
            
        print(f"Received {len(rows)} rows for {rng_str}")
        
        for i, row in enumerate(rows):
            actual_row = start_row + i
            if not isinstance(row, list):
                continue
            col_a = row[0] if len(row) > 0 else ""
            col_b = row[1] if len(row) > 1 else ""
            col_c = row[2] if len(row) > 2 else ""
            col_d = row[3] if len(row) > 3 else ""
            
            # Check valid url in col_b
            if not col_b or not col_b.strip().startswith("http"):
                continue
            
            total_valid_rows += 1
            status = col_d.strip() if col_d else ""
            
            is_queued = (status in ["В очереди", ""])
            if is_queued:
                total_queued += 1
                if first_target is None:
                    first_target = {
                        "row_num": actual_row,
                        "title_orig": col_a.strip(),
                        "url_orig": col_b.strip(),
                        "lang": col_c.strip() if col_c.strip() else "English",
                        "status": status
                    }
    
    print("\n--- SUMMARY ---")
    print(f"Total valid articles with URLs: {total_valid_rows}")
    print(f"Total queued articles: {total_queued}")
    if first_target:
        print("First target to process:", json.dumps(first_target, ensure_ascii=False, indent=2))
    else:
        print("No queued article found.")

if __name__ == "__main__":
    main()
