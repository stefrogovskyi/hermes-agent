import json
import subprocess
import sys

def run_cmd(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    if result.returncode != 0:
        print(f"Error executing command: {cmd}\n{result.stderr}")
        return None
    return result.stdout

def scan_sheet():
    sheet_id = "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k"
    script_path = "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py"
    
    ranges = [
        "'Блогпосты Сирейтс'!A2:G5001",
        "'Блогпосты Сирейтс'!A5002:G10001",
        "'Блогпосты Сирейтс'!A10002:G15001",
        "'Блогпосты Сирейтс'!A15002:G20001",
        "'Блогпосты Сирейтс'!A20002:G23217"
    ]
    
    first_target = None
    total_in_queue = 0
    total_valid_rows = 0
    
    for r_idx, r in enumerate(ranges):
        start_row = [2, 5002, 10002, 15002, 20002][r_idx]
        cmd = f"python3 {script_path} sheets get {sheet_id} \"{r}\""
        output = run_cmd(cmd)
        if not output:
            continue
        try:
            data = json.loads(output)
        except Exception as e:
            print(f"Failed to parse JSON for range {r}: {e}")
            continue
            
        for offset, row in enumerate(data):
            current_row_num = start_row + offset
            if not row:
                continue
            
            # Extract fields
            title_orig = row[0].strip() if len(row) > 0 and row[0] else ""
            url_orig = row[1].strip() if len(row) > 1 and row[1] else ""
            lang = row[2].strip() if len(row) > 2 and row[2] else ""
            status = row[3].strip() if len(row) > 3 and row[3] else ""
            
            # Check if valid row
            if not url_orig or not url_orig.startswith("http"):
                continue
                
            total_valid_rows += 1
            
            # Status check: "В очереди", empty, or missing
            is_queued = (status in ["В очереди", ""] or not status)
            
            if is_queued:
                total_in_queue += 1
                if first_target is None:
                    first_target = {
                        "row_num": current_row_num,
                        "title_orig": title_orig,
                        "url_orig": url_orig,
                        "lang": lang,
                        "status": status
                    }
                    
    print(f"Target row: {first_target}")
    print(f"Total in queue (including target): {total_in_queue}")
    print(f"Total valid rows: {total_valid_rows}")
    
    if first_target:
        with open("/opt/hermes/profiles/archie/target_article.json", "w", encoding="utf-8") as f:
            json.dump({
                "target": first_target,
                "total_in_queue": total_in_queue
            }, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    scan_sheet()
