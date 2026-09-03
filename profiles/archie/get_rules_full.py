import glob, re

files = sorted(glob.glob('/opt/hermes/profiles/archie/cache/delegation/live/deleg_*/task-0.log'))
for fpath in files:
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        txt = f.read()
        if 'MANDATORY RULES' in txt:
            p = txt.find('1.')
            if p != -1:
                print("FILE:", fpath)
                lines = txt[p:].splitlines()
                for l in lines[:20]:
                    print(l)
                break
