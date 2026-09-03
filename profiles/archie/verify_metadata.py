import json

with open('/opt/hermes/profiles/archie/final_output.json', 'r') as f:
    data = json.load(f)

print("Title:", data.get("title"))
print("Meta Title:", data.get("meta_title"))
print("Meta Description:", data.get("meta_description"))
