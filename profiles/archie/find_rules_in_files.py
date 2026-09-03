import glob, re

for fpath in glob.glob('/opt/hermes/profiles/archie/*.py') + glob.glob('/opt/hermes/profiles/archie/*.md'):
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        txt = f.read()
        if 'EM-DASH' in txt and ('Rule 11' in txt or '11.' in txt or '11 rules' in txt):
            print("=== FILE:", fpath)
            lines = [line for line in txt.splitlines() if any(k in line for k in ['1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.'])]
            print("\n".join(lines[:15]))
