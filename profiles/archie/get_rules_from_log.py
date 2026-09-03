import re

log_path = "/opt/hermes/profiles/archie/cache/delegation/live/deleg_33ab14fb/task-0.log"
with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# find where "1." or "8-ШАГ" or "avalanche-copywriting" occurs
idx = text.find("avalanche-copywriting")
if idx != -1:
    print(text[idx:idx+4000])
else:
    print("Not found directly, searching rules...")
    idx2 = text.find("11 rules")
    if idx2 != -1:
        print(text[idx2-500:idx2+3500])
