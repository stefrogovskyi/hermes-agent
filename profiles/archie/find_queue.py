import json, subprocess, sys

sheet_id = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
tab_name = 'Блогпосты Сирейтс'

batch_size = 5000
start_row = 2
max_row = 23217

first_target = None
queued_count = 0

for b_start in range(start_row, max_row + 1, batch_size):
    b_end = min(b_start + batch_size - 1, max_row)
    rng = f"'{tab_name}'!A{b_start}:F{b_end}"
    print(f'Fetching {rng}...')
    cmd = ['python3', '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py', 'sheets', 'get', sheet_id, rng]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f'Error fetching range {rng}: {res.stderr}')
        sys.exit(1)
    
    data = json.loads(res.stdout)
    if isinstance(data, list):
        values = data
    elif isinstance(data, dict):
        values = data.get('values', [])
    else:
        values = []
    
    for idx, row in enumerate(values):
        current_row_num = b_start + idx
        col_a = row[0] if len(row) > 0 else ''
        col_b = row[1] if len(row) > 1 else ''
        col_c = row[2] if len(row) > 2 else ''
        col_d = row[3] if len(row) > 3 else ''
        col_e = row[4] if len(row) > 4 else ''
        col_f = row[5] if len(row) > 5 else ''
        
        has_url = isinstance(col_b, str) and col_b.strip().startswith('http')
        status = col_d.strip() if isinstance(col_d, str) else ''
        
        if has_url and (status in ['В очереди', '', 'в очереди'] or status is None):
            queued_count += 1
            if first_target is None:
                first_target = {
                    'row_num': current_row_num,
                    'orig_title': col_a,
                    'url': col_b,
                    'lang': col_c,
                    'status': status,
                    'navo_title': col_e,
                    'navo_link': col_f
                }

print('FINISHED SEARCH')
print(json.dumps({'first_target': first_target, 'queued_count': queued_count}, ensure_ascii=False, indent=2))
