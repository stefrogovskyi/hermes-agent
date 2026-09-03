import json, os, re

# Let's search in sessions logs or snapshot for the exact 11 rules text
snapshot_path = '/opt/hermes/profiles/archie/.skills_prompt_snapshot.json'
if os.path.exists(snapshot_path):
    with open(snapshot_path) as f:
        txt = f.read()
        print("Snapshot size:", len(txt))

# Let's search terminal logs for "11 rules" or "8-ШАГ"
log_path = '/opt/hermes/profiles/archie/cache/terminal-output/out-1788309323-3652763-5580.log'
if os.path.exists(log_path):
    with open(log_path) as f:
        log_txt = f.read()
        idx = log_txt.find("8-ШАГ")
        if idx != -1:
            print("Found 8-ШАГ at", idx)
            print(log_txt[idx-100:idx+3000])
        else:
            idx2 = log_txt.find("STRICT RULES TO FOLLOW")
            if idx2 != -1:
                print("Found STRICT RULES at", idx2)
                print(log_txt[idx2:idx2+3000])
