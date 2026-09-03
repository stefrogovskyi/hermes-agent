import glob, re

logs = glob.glob('/opt/hermes/profiles/archie/cache/terminal-output/*.log')
for l in sorted(logs):
    with open(l, errors='ignore') as f:
        txt = f.read()
        if "1. " in txt and "11. " in txt:
            p1 = txt.find("1. ")
            p11 = txt.find("11. ", p1)
            if p1 != -1 and p11 != -1 and (p11 - p1 < 4000):
                print(f"=== {l} ===")
                print(txt[p1:p11+300])
                break
