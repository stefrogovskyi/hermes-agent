import subprocess
import json

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
ranges = [
    "'Блогпосты Сирейтс'!A2:G5000",
    "'Блогпосты Сирейтс'!A5001:G10000",
    "'Блогпосты Сирейтс'!A10001:G15000",
    "'Блогпосты Сирейтс'!A15001:G20000",
    "'Блогпосты Сирейтс'!A20001:G23217"
]

found_row = None
total_in_queue = 0

for r_idx, r in enumerate(ranges):
    cmd = ['python3', '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py', 'sheets', 'get', SHEET_ID, r]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching {r}: {res.stderr}")
        continue
    data = json.loads(res.stdout)
    if isinstance(data, dict):
        values = data.get('values', [])
    elif isinstance(data, list):
        values = data
    else:
        values = []
    
    start_row = 2 if r_idx == 0 else (5001 if r_idx == 1 else (10001 if r_idx == 2 else (15001 if r_idx == 3 else 20001)))
    
    for idx, row in enumerate(values):
        row_num = start_row + idx
        title = row[0].strip() if len(row) > 0 else ''
        url = row[1].strip() if len(row) > 1 else ''
        lang = row[2].strip() if len(row) > 2 else ''
        status = row[3].strip() if len(row) > 3 else ''
        
        if not url or not url.startswith('http'):
            continue
            
        if status in ['В очереди', ''] or not status:
            total_in_queue += 1
            if found_row is None:
                found_row = {
                    "row_num": row_num,
                    "title": title,
                    "url": url,
                    "lang": lang,
                    "status": status
                }

print("FOUND CANDIDATE:", json.dumps(found_row, ensure_ascii=False))
print("TOTAL IN QUEUE AT START:", total_in_queue)

with open('/opt/hermes/profiles/archie/found_candidate.json', 'w', encoding='utf-8') as f:
    json.dump({'found_row': found_row, 'total_in_queue': total_in_queue}, f, ensure_ascii=False, indent=2)
