import subprocess
import json
import sys

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
CLI = '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py'

def read_range(rng):
    cmd = ['python3', CLI, 'sheets', 'get', SHEET_ID, f'Блогпосты Сирейтс!{rng}']
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        return None
    try:
        return json.loads(res.stdout)
    except Exception:
        return None

def count_remaining():
    batch_size = 5000
    start_row = 2
    max_row = 23217
    
    queue_count = 0
    curr = start_row
    while curr <= max_row:
        end = min(curr + batch_size - 1, max_row)
        rows = read_range(f'A{curr}:G{end}')
        if not rows:
            break
            
        for row in rows:
            link = row[1] if len(row) > 1 else ""
            status = row[3] if len(row) > 3 else ""
            
            if not link or not link.strip().startswith('http'):
                continue
                
            status_clean = status.strip()
            if status_clean == "" or status_clean == "В очереди":
                queue_count += 1
                    
        curr = end + 1
        
    return queue_count

if __name__ == '__main__':
    remaining = count_remaining()
    print(f"REMAINING_QUEUE_COUNT: {remaining}")
