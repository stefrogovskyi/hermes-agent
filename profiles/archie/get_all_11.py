with open('/opt/hermes/profiles/archie/cache/terminal-output/out-1788160440-3216452-28a0.log') as f:
    text = f.read()

import re
matches = re.findall(r'1\. STRICT.*?(?=Goal:|===|\Z)', text, re.DOTALL)
for i, m in enumerate(matches):
    print(f"--- MATCH {i} ---")
    print(m[:1500])
