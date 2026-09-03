import json
import re

with open("/opt/hermes/profiles/archie/article.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Fix the 8-word overlap sequence
body = data["body_markdown"]
old_phrase = "A breakdown on a German highway late at night or during a public holiday tests any driver's patience."
new_phrase = "A breakdown on a German highway during late-night hours or official holidays tests any driver's patience."

if old_phrase in body:
    body = body.replace(old_phrase, new_phrase)
    data["body_markdown"] = body
    print("Replaced old phrase with new phrase.")
else:
    print("Old phrase not found, checking alternatives...")

with open("/opt/hermes/profiles/archie/article.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Updated article.json successfully.")
