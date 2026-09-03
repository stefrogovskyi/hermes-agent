import json
import re

with open("candidate_draft.json", "r") as f:
    data = json.load(f)

body = data["body_markdown"]

# Fix identified audit items
body = body.replace("dispatch management systems", "inventory management systems")
body = body.replace("office building", "apartment building")

data["body_markdown"] = body

with open("candidate_draft.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Updated candidate_draft.json with fixes.")
