import subprocess
import json
import sys

sheet_id = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
cmd_base = ['python3', '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py', 'sheets', 'get', sheet_id]

batch_size = 5000
start_row = 2
max_row = 23217

first_target = None
in_queue_count = 0

curr = start_row
while curr <= max_row:
    end = min(curr + batch_size - 1, max_row)
    range_str = f"'Блогпосты Сирейтс'!A{curr}:G{end}"
    res = subprocess.run(cmd_base + [range_str], capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching {range_str}: {res.stderr}", file=sys.stderr)
        break
    try:
        data = json.loads(res.stdout)
    except Exception as e:
        print(f"JSON decode error: {e}", file=sys.stderr)
        break

    if not isinstance(data, list):
        print(f"Unexpected output format: {type(data)}", file=sys.stderr)
        break
    
    for idx, row in enumerate(data):
        row_num = curr + idx
        title_orig = row[0] if len(row) > 0 else ''
        url_orig = row[1] if len(row) > 1 else ''
        lang = row[2] if len(row) > 2 else ''
        status = row[3] if len(row) > 3 else ''
        
        if not url_orig or not str(url_orig).startswith('http'):
            continue
            
        status_clean = str(status).strip() if status else ''
        if status_clean in ['В очереди', '']:
            in_queue_count += 1
            if first_target is None:
                first_target = {
                    'row_num': row_num,
                    'title_orig': title_orig,
                    'url_orig': url_orig,
                    'lang': lang,
                    'status': status_clean
                }
    curr = end + 1

print(json.dumps({'first_target': first_target, 'in_queue_count': in_queue_count}))
