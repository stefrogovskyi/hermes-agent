import subprocess
import json
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
SCRIPT_PATH = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_sheet_range(rng):
    cmd = ["python3", SCRIPT_PATH, "sheets", "get", SHEET_ID, f"'{TAB_NAME}'!{rng}"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Error getting range:", res.stderr)
        return []
    try:
        data = json.loads(res.stdout)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return data.get("values", [])
        return []
    except Exception as e:
        print("Error parsing JSON:", e)
        print("Stdout preview:", res.stdout[:500])
        return []

def main():
    start_row = 2
    max_row = 23217
    batch_size = 5000
    
    target_row = None
    target_data = None
    
    total_in_queue = 0
    
    curr = start_row
    while curr <= max_row:
        end = min(curr + batch_size - 1, max_row)
        rng_str = f"A{curr}:G{end}"
        print(f"Reading batch A{curr}:G{end}...")
        rows = get_sheet_range(rng_str)
        if not rows:
            print(f"Empty or error fetching {rng_str}")
            # If batch fails or is empty, break if past known range or continue
            
        for i, r in enumerate(rows):
            actual_row = curr + i
            # r: A=Title(0), B=URL(1), C=Lang(2), D=Status(3), E=Navo Title(4), F=Navo Link(5)
            col_b = r[1].strip() if len(r) > 1 else ""
            col_d = r[3].strip() if len(r) > 3 else ""
            
            # Check if valid URL in B
            if not col_b or not (col_b.startswith("http://") or col_b.startswith("https://")):
                continue
                
            is_unprocessed = col_d in ["В очереди", "", None]
            if is_unprocessed:
                total_in_queue += 1
                if target_row is None:
                    target_row = actual_row
                    target_data = {
                        "row": actual_row,
                        "title_orig": r[0] if len(r) > 0 else "",
                        "url_orig": col_b,
                        "lang": r[2] if len(r) > 2 else "English",
                        "status": col_d
                    }
        curr = end + 1
        
    print(f"Total in queue found across all checked rows: {total_in_queue}")
    if target_row is None or target_data is None:
        print("QUEUE_EMPTY")
        sys.exit(0)
        
    print("TARGET_FOUND:", json.dumps(target_data, ensure_ascii=False))
    
    # Save target info to json file for reference
    with open("/opt/hermes/profiles/archie/current_article.json", "w") as f:
        target_data["total_in_queue"] = total_in_queue
        json.dump(target_data, f, ensure_ascii=False, indent=2)

    # Update status to "В процессе"
    update_rng = f"D{target_row}"
    update_cmd = ["python3", SCRIPT_PATH, "sheets", "update", "--values", '[["В процессе"]]', SHEET_ID, f"'{TAB_NAME}'!{update_rng}"]
    res_up = subprocess.run(update_cmd, capture_output=True, text=True)
    if res_up.returncode == 0:
        print(f"Successfully locked row {target_row} to 'В процессе'")
    else:
        print(f"Failed to lock row {target_row}: {res_up.stderr}")

if __name__ == "__main__":
    main()
