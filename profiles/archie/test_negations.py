import json
import re

with open("draft.json") as f:
    data = json.load(f)

text = data["body_markdown"]

# Find all occurrences of "not", "n't", "rather than", "instead of"
lines = text.split("\n")
for line_num, line in enumerate(lines, 1):
    if re.search(r'\b(not|n\'t|rather than|instead of)\b', line, re.I):
        print(f"Line {line_num}: {line}")

