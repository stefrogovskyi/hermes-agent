import subprocess
import json
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB_NAME = "Блогпосты Сирейтс"
SCRIPT_PATH = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_range(start_row, end_row):
    range_str = f"'{TAB_NAME}'!A{start_row}:G{end_row}"
    cmd = [
        "python3", SCRIPT_PATH,
        "sheets", "get",
        SHEET_ID,
        range_str
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error reading {range_str}: {res.stderr}")
        return None
    try:
        data = json.loads(res.stdout)
        return data
    except Exception as e:
        print(f"JSON parse error for {range_str}: {e}")
        return None

def main():
    total_in_queue = 0
    selected_row = None
    selected_data = None

    # Step in chunks of 5000 from 2 to 23217
    chunks = [
        (2, 5001),
        (5002, 10001),
        (10002, 15001),
        (15002, 20001),
        (20002, 23217)
    ]

    for start_r, end_r in chunks:
        print(f"Fetching range A{start_r}:G{end_r}...")
        rows = get_range(start_r, end_r)
        if not rows or not isinstance(rows, list):
            print("Failed to fetch chunk or empty, retrying or exiting.")
            continue
        
        for i, row in enumerate(rows):
            row_idx = start_r + i
            # Row columns:
            # A (0): Title (orig)
            # B (1): Link (orig)
            # C (2): Language
            # D (3): Status
            # E (4): Title (Navo)
            # F (5): Link (Navo/File Navo)
            
            if not row or len(row) < 2:
                continue
            
            orig_title = row[0].strip() if len(row) > 0 else ""
            orig_url = row[1].strip() if len(row) > 1 else ""
            lang = row[2].strip() if len(row) > 2 else ""
            status = row[3].strip() if len(row) > 3 else ""

            # Check valid URL in B
            if not orig_url.startswith("http"):
                continue

            # Queue condition: Status is "В очереди", empty, or missing
            if status in ["В очереди", ""]:
                total_in_queue += 1
                if selected_row is None:
                    selected_row = row_idx
                    selected_data = {
                        "row_idx": row_idx,
                        "title": orig_title,
                        "url": orig_url,
                        "lang": lang,
                        "status": status
                    }

    print(f"Scan complete. Total in queue: {total_in_queue}")
    if selected_row:
        print(f"Selected Row: {selected_row}")
        print(f"Details: {json.dumps(selected_data, ensure_ascii=False, indent=2)}")
        with open("/opt/hermes/profiles/archie/target_article.json", "w") as f:
            json.dump({"selected": selected_data, "total_in_queue": total_in_queue}, f, ensure_ascii=False, indent=2)
    else:
        print("QUEUE IS EMPTY! All articles processed.")

if __name__ == "__main__":
    main()
