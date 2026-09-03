import json

with open("final_verified_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Replace 'tens of thousands of dollars'
data["body_markdown"] = data["body_markdown"].replace(
    "tens of thousands of dollars in losses",
    "heavy financial sums exceeding tens of thousands daily"
)

with open("final_verified_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated final_verified_data.json!")
