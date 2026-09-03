import json

# Read output.json from working directory if it exists, or parse from summary file
try:
    with open("output.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    print("Found output.json from subagent!")
except Exception as e:
    print("Could not load output.json, extracting from summary...")
    with open("cache/delegation/subagent-summary-0-20260902_060516_950518.txt", "r", encoding="utf-8") as f:
        summary = f.read()
    json_str = summary.split("```json")[1].split("```")[0].strip()
    data = json.loads(json_str)

with open("rewrite_v1.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Title:", data["title"])
print("Meta Title:", data["meta_title"])
print("Meta Description:", data["meta_description"])
print("Body length:", len(data["body"]))
