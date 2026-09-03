import subprocess
import json

def find_queue():
    cmd = ['python3', '/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py', 'sheets', 'get', '1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k', "'Блогпосты Сирейтс'!A2:G23217"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print('Error:', res.stderr)
        return
    
    data = json.loads(res.stdout)
    print(f'Total rows returned: {len(data)}')
    
    first_target = None
    first_row_num = None
    queue_count = 0
    
    for idx, row in enumerate(data, start=2):
        title = row[0] if len(row) > 0 else ''
        url = row[1] if len(row) > 1 else ''
        lang = row[2] if len(row) > 2 else ''
        status = row[3] if len(row) > 3 else ''
        
        # Check if valid url
        if not url or not url.startswith('http'):
            continue
            
        status_clean = status.strip() if status else ''
        if status_clean in ['В очереди', '', 'pending', 'Pending']:
            queue_count += 1
            if first_target is None:
                first_target = (row, idx)
                first_row_num = idx

    print(f'Queue count: {queue_count}')
    if first_target:
        print(f'First match at row {first_row_num}: {first_target[0]}')
        with open('/opt/hermes/profiles/archie/next_target.json', 'w') as f:
            json.dump({
                'row_num': first_row_num,
                'title': first_target[0][0] if len(first_target[0]) > 0 else '',
                'url': first_target[0][1] if len(first_target[0]) > 1 else '',
                'lang': first_target[0][2] if len(first_target[0]) > 2 else '',
                'status': first_target[0][3] if len(first_target[0]) > 3 else '',
                'queue_count': queue_count
            }, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    find_queue()
