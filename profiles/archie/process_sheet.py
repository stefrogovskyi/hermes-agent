import subprocess
import json
import sys

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
CLI = '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py'

def read_range(rng):
    cmd = ['python3', CLI, 'sheets', 'get', SHEET_ID, f'Блогпосты Сирейтс!{rng}']
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error reading range {rng}: {res.stderr}", file=sys.stderr)
        return None
    try:
        return json.loads(res.stdout)
    except Exception as e:
        print(f"JSON decode error: {e}", file=sys.stderr)
        return None

def scan_queue():
    batch_size = 5000
    start_row = 2
    max_row = 23217
    
    first_target = None
    queue_count = 0
    
    curr = start_row
    while curr <= max_row:
        end = min(curr + batch_size - 1, max_row)
        rng = f'A{curr}:G{end}'
        print(f"Reading range: {rng}...", file=sys.stderr)
        rows = read_range(rng)
        if not rows:
            print(f"Failed to read batch {rng}", file=sys.stderr)
            break
            
        for idx, row in enumerate(rows):
            actual_row = curr + idx
            title = row[0] if len(row) > 0 else ""
            link = row[1] if len(row) > 1 else ""
            lang = row[2] if len(row) > 2 else ""
            status = row[3] if len(row) > 3 else ""
            
            # Check validity
            if not link or not link.strip().startswith('http'):
                continue
                
            status_clean = status.strip()
            if status_clean == "" or status_clean == "В очереди":
                queue_count += 1
                if first_target is None:
                    first_target = {
                        'row_num': actual_row,
                        'title': title,
                        'link': link,
                        'lang': lang,
                        'status': status
                    }
                    
        curr = end + 1
        
    return first_target, queue_count

if __name__ == '__main__':
    target, count = scan_queue()
    result = {
        'target': target,
        'queue_count': count
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
