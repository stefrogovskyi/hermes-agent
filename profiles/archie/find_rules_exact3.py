import os, re

for root, dirs, filenames in os.walk('/opt/hermes/profiles/archie'):
    for fn in filenames:
        if fn.endswith('.log') or fn.endswith('.json') or fn.endswith('.txt') or fn.endswith('.md'):
            fpath = os.path.join(root, fn)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    if 'Rule 1:' in content or '1. NO EM-DASH' in content or '1. ABSOLUTE' in content or '1. STRICT ZERO EM-DASH' in content:
                        print(f"MATCH IN {fpath}:")
                        m = re.search(r'(1\.\s+.*?(?=8-step|Audit|LAYER|\Z))', content, re.DOTALL)
                        if m:
                            print(m.group(0)[:2000])
                            print("="*50)
            except Exception as e:
                pass
