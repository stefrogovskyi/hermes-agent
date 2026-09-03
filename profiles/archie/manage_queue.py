import json
import subprocess
import sys

SHEET_ID = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
GOOGLE_API_CLI = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"

def run_cmd(cmd):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"Command failed: {p.stderr}")
    return p.stdout

def find_first_queued():
    batch_size = 5000
    start_row = 2
    max_row = 23217
    
    total_queued = 0
    first_found = None
    
    while start_row <= max_row:
        end_row = min(start_row + batch_size - 1, max_row)
        range_name = f"'Блогпосты Сирейтс'!A{start_row}:G{end_row}"
        print(f"Fetching range {range_name}...", file=sys.stderr)
        
        cmd = f"python3 {GOOGLE_API_CLI} sheets get {SHEET_ID} \"{range_name}\""
        out = run_cmd(cmd)
        data = json.loads(out)
        
        for idx, row in enumerate(data):
            curr_row_num = start_row + idx
            title = row[0] if len(row) > 0 else ""
            link = row[1] if len(row) > 1 else ""
            lang = row[2] if len(row) > 2 else ""
            status = row[3] if len(row) > 3 else ""
            
            # Check validity
            if not link or not link.startswith("http"):
                continue # Artifact / invalid row
                
            status_clean = status.strip()
            if status_clean in ["В очереди", "", None] or not status_clean:
                total_queued += 1
                if first_found is None:
                    first_found = {
                        "row_num": curr_row_num,
                        "title": title,
                        "link": link,
                        "lang": lang,
                        "status": status
                    }
        
        start_row = end_row + 1

    return first_found, total_queued

if __name__ == "__main__":
    found, remaining = find_first_queued()
    print(json.dumps({"first_found": found, "remaining_count": remaining}, ensure_ascii=False, indent=2))
