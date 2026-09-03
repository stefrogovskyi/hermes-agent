import json, glob

files = sorted(glob.glob('/opt/hermes/profiles/archie/cache/delegation/live/*/task-0.log'))
for f in files:
    with open(f) as fp:
        txt = fp.read()
        if 'MANDATORY RULES' in txt:
            p = txt.find('MANDATORY RULES')
            print(f"=== {f} ===")
            print(txt[p:p+2500])
            break
