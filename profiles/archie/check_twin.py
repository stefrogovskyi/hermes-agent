import json
import re

with open("output.json") as f:
    data = json.load(f)

body = data["body_markdown"]
lines = body.split("\n")

for line in lines:
    line = line.strip()
    if not line or line.startswith("#") or line.startswith("*"):
        continue
    sentences = re.split(r'(?<=[.!?])\s+', line)
    if len(sentences) > 1:
        print("--- PARAGRAPH ---")
        for i, s in enumerate(sentences):
            words = s.split()
            first_two = " ".join(words[:2]) if len(words) >= 2 else ""
            last_two = " ".join(words[-2:]) if len(words) >= 2 else ""
            print(f"  S{i+1}: {s}")
            print(f"      First 2: '{first_two}' | Last 2: '{last_two}' | Length: {len(words)}")

