import glob, re

logs = glob.glob('/opt/hermes/profiles/archie/cache/terminal-output/*.log')
for l in logs:
    with open(l) as f:
        txt = f.read()
        if "11 Anti-AI Copywriting Rules" in txt or "11 rules" in txt:
            idx = txt.find("1. ABSOLUTE PROHIBITION")
            if idx != -1:
                print("FOUND RULES IN LOG:", l)
                print(txt[idx:idx+4000])
                break
