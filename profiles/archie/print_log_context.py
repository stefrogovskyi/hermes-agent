import re

with open('/opt/hermes/profiles/archie/cache/delegation/live/deleg_c083a1ce/task-0.log', 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Print context portion
m = re.search(r'context:.*', text)
if m:
    print(m.group(0))
