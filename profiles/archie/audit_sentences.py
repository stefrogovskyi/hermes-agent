import re
from audit_layer2 import body_text, title, meta_title, meta_desc

full_text = f"{title}\n{meta_title}\n{meta_desc}\n\n{body_text}"
paragraphs = full_text.split('\n\n')

for i, p in enumerate(paragraphs):
    print(f"--- Paragraph / Block {i+1} ---")
    print(p.strip())
    print()

