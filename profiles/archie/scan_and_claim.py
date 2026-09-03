import subprocess
import json
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
TAB = "Блогпосты Сирейтс"
GOOGLE_API = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def get_range(range_str):
    cmd = ["python3", GOOGLE_API, "sheets", "get", SHEET_ID, f"{TAB}!{range_str}"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Error fetching range {range_str}: {res.stderr}")
    return json.loads(res.stdout)

def main():
    print("Fetching sheet data in batches...")
    all_rows = []
    # Read in batches of 5000: A2:G5001, A5002:G10001, A10002:G15001, A15002:G20001, A20002:G23217
    ranges = [
        "A2:G5001",
        "A5002:G10001",
        "A10002:G15001",
        "A15002:G20001",
        "A20002:G23217"
    ]
    
    total_queued = 0
    candidate = None
    
    start_row = 2
    for r in ranges:
        data = get_range(r)
        # data is array of rows
        for offset, row in enumerate(data):
            row_idx = start_row + offset
            title_orig = row[0] if len(row) > 0 else ""
            url_orig = row[1] if len(row) > 1 else ""
            lang = row[2] if len(row) > 2 else ""
            status = row[3] if len(row) > 3 else ""
            
            status_clean = status.strip().lower() if status else ""
            
            # Valid item has valid URL in B
            if not url_orig or not url_orig.strip().startswith("http"):
                continue
                
            if status_clean in ["в очереди", "queued", "in queue", ""]:
                total_queued += 1
                if candidate is None:
                    candidate = {
                        "row_idx": row_idx,
                        "title_orig": title_orig,
                        "url_orig": url_orig,
                        "lang": lang,
                        "status": status
                    }
        start_row += len(data)

    print(f"Total queued items remaining: {total_queued}")
    if candidate is None:
        print("NO_CANDIDATE_FOUND")
        return

    print(f"Selected Candidate at Row {candidate['row_idx']}:")
    print(json.dumps(candidate, ensure_ascii=False, indent=2))
    
    # Write selected candidate info to file
    with open("claimed_article.json", "w", encoding="utf-8") as f:
        json.dump({"candidate": candidate, "total_queued": total_queued}, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
