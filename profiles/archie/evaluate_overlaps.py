from audit_script import original, candidate
from detailed_audit import matches

print("Evaluating 17 matches against exclusions (proper nouns, carrier lists, tool names, fixed API status codes):")
non_exempt = []
for idx, m in enumerate(matches):
    cand_pos, orig_pos, length, text = m
    print(f"\nMatch #{idx+1} [Len: {length}]:")
    print(f"  Text: '{text}'")
    
# Let's inspect each manually or classify
