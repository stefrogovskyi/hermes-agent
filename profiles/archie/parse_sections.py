import json

with open("test_full_check.py") as f:
    code = f.read()

# Execute body from test_full_check
loc = {}
exec(code, loc)
body = loc['body']

headers = [
    "Line Item Confusion and Description Gaps",
    "The Customs Valuation Baseline and Dutiable Extras",
    "Mandatory Regulatory Approvals and Special Authorizations",
    "Deadlines and the Pre-Arrival Critical Path",
    "Routine Clearance Protocols"
]

# Split body by headers
current = body
section_map = {}

for i, h in enumerate(headers):
    parts = current.split(h)
    if i == 0:
        section_map["Intro"] = parts[0].strip()
    current = parts[1]
    if i < len(headers) - 1:
        next_h = headers[i+1]
        sec_content = current.split(next_h)[0]
        section_map[h] = sec_content.strip()
    else:
        section_map[h] = current.strip()

for h, content in section_map.items():
    paras = [p.strip() for p in content.split('\n\n') if p.strip()]
    print(f"[{h}] -> {len(paras)} paragraph(s):")
    for idx, p in enumerate(paras):
        first_line = p.split('\n')[0][:50]
        print(f"  P{idx+1}: {first_line}...")
    print()

