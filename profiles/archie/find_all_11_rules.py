import os, re

files = []
for root, dirs, filenames in os.walk('/opt/hermes/profiles/archie/cache/'):
    for fn in filenames:
        if fn.endswith('.log') or fn.endswith('.json') or fn.endswith('.txt'):
            files.append(os.path.join(root, fn))

for fpath in files:
    try:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if 'Rule 11' in content or '11. ' in content:
                # search for a sequence where 1. and 11. exist
                pos1 = content.find('1.')
                pos11 = content.find('11.')
                if pos1 != -1 and pos11 != -1 and pos1 < pos11 and (pos11 - pos1) < 5000:
                    print(f"FOUND IN {fpath}:")
                    print(content[pos1:pos11+300])
                    print("="*50)
                    break
    except Exception as e:
        pass
