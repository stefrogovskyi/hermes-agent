import json

with open('/opt/hermes/profiles/archie/rewrite_draft.json') as f:
    data = json.load(f)

print("TITLE:", data.get("title"))
print("META TITLE:", data.get("meta_title"))
print("META DESCRIPTION:", data.get("meta_description"))
print("\n--- BODY ---")
print(data.get("body"))
