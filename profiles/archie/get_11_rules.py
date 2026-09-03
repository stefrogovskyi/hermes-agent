import glob, re

logs = glob.glob('/opt/hermes/profiles/archie/cache/terminal-output/*.log')
for l in logs:
    with open(l) as f:
        txt = f.read()
        if "1. NO EM-DASH" in txt and "11." in txt:
            p1 = txt.find("1. NO EM-DASH")
            p11 = txt.find("11.", p1)
            if p1 != -1 and p11 != -1 and (p11 - p1 < 3000):
                print("FOUND ALL 11 RULES IN LOG:", l)
                print(txt[p1:p11+200])
                break
