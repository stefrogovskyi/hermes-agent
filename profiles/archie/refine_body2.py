import json

with open('/opt/hermes/profiles/archie/rewrite_draft.json', 'r') as f:
    draft = json.load(f)

body = draft['body']

# Refine port list
body = body.replace(
    "smart ports such as Singapore, Rotterdam, and Shanghai rely on",
    "automated maritime hubs including Rotterdam, Shanghai, and Singapore utilize"
)

# Refine country list
body = body.replace(
    "Countries including the US, China, Europe, and Brazil compete for",
    "Global powers such as China, Brazil, European nations, and the US compete for"
)

draft['body'] = body

with open('/opt/hermes/profiles/archie/rewrite_draft.json', 'w') as f:
    json.dump(draft, f, indent=2)

print("Refinement 2 applied successfully.")
