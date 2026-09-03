import json

base = "/opt/hermes/profiles/archie/workdir/row69/counts"
files = ["b1.json", "b2.json", "b3.json", "b4.json", "b5.json"]

total_rows = 0
status_counts = {}
queue_count = 0
done_count = 0
in_progress_count = 0
error_count = 0
empty_or_junk = 0

for fname in files:
    with open(f"{base}/{fname}") as f:
        values = json.load(f)
    for row in values:
        total_rows += 1
        row_padded = row + [''] * (7 - len(row))
        a, b, c, d, e, f_, g = row_padded[:7]
        b = b.strip()
        d = d.strip()
        if not b:
            empty_or_junk += 1
            continue
        status_counts[d] = status_counts.get(d, 0) + 1
        if not d or d.lower() in ['в очереди', 'queue', 'queued']:
            queue_count += 1
        elif d == 'Готово':
            done_count += 1
        elif d == 'В процессе':
            in_progress_count += 1
        elif d == 'Ошибка':
            error_count += 1

print("Total rows scanned:", total_rows)
print("Empty/no-link rows (skipped):", empty_or_junk)
print("Status breakdown:", status_counts)
print()
print("QUEUE (В очереди/empty, valid link):", queue_count)
print("DONE (Готово):", done_count)
print("IN PROGRESS (В процессе):", in_progress_count)
print("ERROR (Ошибка):", error_count)
