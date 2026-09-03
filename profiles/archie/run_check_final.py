import json
from check_script import check_rules

with open("final_output.json") as f:
    data = json.load(f)

errors = check_rules(data)
print("ERRORS ENCOUNTERED:", errors)
print("Title len:", len(data["title"]))
print("Meta title len:", len(data["meta_title"]))
print("Meta desc len:", len(data["meta_description"]))
