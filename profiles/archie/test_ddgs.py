from ddgs import DDGS
import json

queries = [
    "ocean freight rate fluctuation causes",
    "container shipping spot rates volatility factors",
    "global logistics freight rate drivers"
]

results = {}
ddgs = DDGS()
for q in queries:
    try:
        res = ddgs.text(q, max_results=3)
        results[q] = res
    except Exception as e:
        results[q] = str(e)

print(json.dumps(results, indent=2))
with open("keywords_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
