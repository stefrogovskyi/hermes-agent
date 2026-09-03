import subprocess
import json
import sys

def get_sheet_data():
    cmd = [
        "python3",
        "/opt/hermes/profiles/archie/skills/productivity/google-workspace/scripts/google_api.py",
        "sheets", "get",
        "1FI4w3NqDJEzhrqcyJKRWu4sCd57oKSMrfgPEt44b63k",
        "'Блогпосты Сирейтс'!A2:G23217"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Error fetching sheet:", res.stderr)
        sys.exit(1)
    
    rows = json.loads(res.stdout)
    return rows

if __name__ == '__main__':
    rows = get_sheet_data()
    print(f"Total rows fetched: {len(rows)}")
    
    in_queue_count = 0
    done_count = 0
    in_progress_count = 0
    error_count = 0
    first_queue_row = None
    
    for i, row in enumerate(rows):
        row_num = i + 2 # Header is row 1
        col_a = row[0] if len(row) > 0 else ""
        col_b = row[1] if len(row) > 1 else ""
        col_c = row[2] if len(row) > 2 else ""
        col_d = row[3] if len(row) > 3 else ""
        col_e = row[4] if len(row) > 4 else ""
        col_f = row[5] if len(row) > 5 else ""
        
        # Skip garbage/empty rows
        if not col_b or not col_b.strip().startswith("http"):
            continue
            
        status = col_d.strip()
        if status == "В очереди" or status == "":
            in_queue_count += 1
            if first_queue_row is None:
                first_queue_row = (row_num, col_a, col_b, col_c, status)
        elif status == "Готово":
            done_count += 1
        elif status == "В процессе":
            in_progress_count += 1
        elif "Ошибка" in status or status == "Ошибка":
            error_count += 1
            
    print(f"Queue stats: Done={done_count}, InProgress={in_progress_count}, Error={error_count}, InQueue={in_queue_count}")
    if first_queue_row:
        print(f"FIRST QUEUE ROW: Row {first_queue_row[0]}")
        print(f"Title: {first_queue_row[1]}")
        print(f"URL: {first_queue_row[2]}")
        print(f"Lang: {first_queue_row[3]}")
        print(f"Status: '{first_queue_row[4]}'")
    else:
        print("NO QUEUE ROWS FOUND!")
