import json
import subprocess
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
SCRIPT_PATH = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def run_cmd(args):
    res = subprocess.run(args, capture_output=True, text=True)
    if res.returncode != 0:
        print("Error executing command:", args)
        print("Stderr:", res.stderr)
        sys.exit(1)
    return res.stdout

def main():
    range_str = f"'{TAB_NAME}'!A1:G23217"
    stdout = run_cmd(["python3", SCRIPT_PATH, "sheets", "get", SHEET_ID, range_str])
    data = json.loads(stdout)
    
    print(f"Total rows fetched: {len(data)}")
    
    queue_items = []
    target_row = None
    
    for idx, row in enumerate(data[1:], start=2):
        title_orig = row[0].strip() if len(row) > 0 and row[0] else ''
        url_orig = row[1].strip() if len(row) > 1 and row[1] else ''
        lang = row[2].strip() if len(row) > 2 and row[2] else 'English'
        status = row[3].strip() if len(row) > 3 and row[3] else ''
        title_navo = row[4].strip() if len(row) > 4 and row[4] else ''
        link_navo = row[5].strip() if len(row) > 5 and row[5] else ''
        
        # Valid URL check
        if not url_orig or not url_orig.startswith('http'):
            continue
            
        if status in ['В очереди', '', 'None'] or not status:
            queue_items.append((idx, title_orig, url_orig, lang, status))
            if target_row is None:
                target_row = (idx, title_orig, url_orig, lang, status)

    print(f"Total valid articles remaining in queue: {len(queue_items)}")
    
    if not target_row:
        print("QUEUE_EMPTY")
        return

    row_num, title_orig, url_orig, lang, status = target_row
    print(f"Target found at row {row_num}: '{title_orig}' | URL: {url_orig} | Lang: {lang}")
    
    # Mark status as "В процессе"
    update_range = f"'{TAB_NAME}'!D{row_num}"
    update_res = run_cmd(["python3", SCRIPT_PATH, "sheets", "update", SHEET_ID, update_range, "--values", json.dumps([["В процессе"]])])
    print("Status updated to 'В процессе':", update_res.strip())
    
    # Save target info to file for easy access
    target_data = {
        "row_num": row_num,
        "title_orig": title_orig,
        "url_orig": url_orig,
        "lang": lang,
        "total_remaining_in_queue": len(queue_items)
    }
    with open("/opt/hermes/profiles/archie/current_target.json", "w") as f:
        json.dump(target_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
