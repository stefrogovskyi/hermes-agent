import json

with open("article_final.json", "r", encoding="utf-8") as f:
    data = json.load(f)

body = data["body"]

body = body.replace(
    "Location data services received translations across 8 major worldwide languages, covering 217 capitals, 35,000 seaports, and the top 100 world seaports. Search functionality for the top 200+ world seaports was also overhauled for faster autocomplete returns.",
    "Location autocomplete services now offer translations across eight primary languages, spanning 217 capital cities, 35,000 maritime harbors, and 100 key global terminals. Lookup algorithms for over 200 premier international ports were also restructured to accelerate query results."
)

body = body.replace(
    "Freight rate queries process with higher accuracy and return a direct link to the Logistics Explorer interface.",
    "Freight rate queries process with higher accuracy, directing users straight into the Logistics Explorer routing engine."
)

data["body"] = body

with open("article_final.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Updated article_final.json!")
