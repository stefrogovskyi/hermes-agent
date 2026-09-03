import json

with open("rewrite_v1.json", "r", encoding="utf-8") as f:
    rewrite = json.load(f)

body = rewrite["body"]

# Tweak 1: Traze sentence
old_p1 = "While specialized trading entities like Traze manage these movements as routine background operations, shifting freight costs create unpredictability across online sales operations."
new_p1 = "While large trading companies like Traze might be less affected, shifting freight costs create unpredictability for many online traders."

# Tweak 2: Representatives sentence
old_p2 = "Freight companies once posted dockside representatives and truck stop brokers to negotiate shipping prices face to face. Digital freight marketplaces replaced those physical reps."
new_p2 = "Freight companies once posted representatives at docks and truck stops to advertise prices for specific loads. Digital freight marketplaces replaced those physical representatives."

if old_p1 in body:
    body = body.replace(old_p1, new_p1)
    print("Replaced Traze sentence successfully.")
else:
    print("p1 match not found, checking...")

if old_p2 in body:
    body = body.replace(old_p2, new_p2)
    print("Replaced reps sentence successfully.")
else:
    print("p2 match not found, checking...")

rewrite["body"] = body

with open("rewrite_final.json", "w", encoding="utf-8") as f:
    json.dump(rewrite, f, ensure_ascii=False, indent=2)

print("Saved rewrite_final.json successfully!")
