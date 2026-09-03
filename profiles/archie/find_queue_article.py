import subprocess
import json

SHEET_ID = '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k'
SHEET_NAME = 'Блогпосты Сирейтс'
CLI_PATH = '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py'

batch_size = 5000
start_row = 2
end_max = 23217

first_queue_row = None
first_queue_data = None
total_in_queue = 0
total_valid_rows = 0

for b_start in range(start_row, end_max + 1, batch_size):
    b_end = min(b_start + batch_size - 1, end_max)
    range_str = f"'{SHEET_NAME}'!A{b_start}:G{b_end}"
    cmd = ['python3', CLI_PATH, 'sheets', 'get', SHEET_ID, range_str]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Error fetching {range_str}: {res.stderr}")
        break
    data = json.loads(res.stdout)
    for idx, row in enumerate(data):
        current_row_num = b_start + idx
        col_b = row[1].strip() if len(row) > 1 and row[1] else ''
        col_d = row[3].strip() if len(row) > 3 and row[3] else ''
        
        if not col_b.startswith('http'):
            continue
            
        total_valid_rows += 1
        
        is_queue = col_d == '' or col_d.lower() == 'в очереди'
        if is_queue:
            total_in_queue += 1
            if first_queue_row is None:
                first_queue_row = current_row_num
                first_queue_data = row

print(json.dumps({
    "first_queue_row": first_queue_row,
    "first_queue_data": first_queue_data,
    "total_in_queue": total_in_queue,
    "total_valid_rows": total_valid_rows
}, ensure_ascii=False, indent=2))
