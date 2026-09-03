import json

with open('/opt/hermes/profiles/archie/rewrite_draft.json', 'r') as f:
    draft = json.load(f)

body = draft['body']

# 1. Replace "smart ports such as singapore, rotterdam, and shanghai"
body = body.replace("major maritime hubs like Singapore, Rotterdam, and Shanghai", "major global ports including Rotterdam, Shanghai, and Singapore")

# 2. Replace "the US, China, Europe, and Brazil"
body = body.replace("critical for the US, China, Europe, and Brazil", "vital for regional powers including China, Brazil, Europe, and the United States")

# 3. Replace "equivalent to 4 football fields"
body = body.replace("(equivalent to 4 football fields)", "(spanning approximately four football fields)")

# 4. Replace "drilling systems, autonomous underwater drones"
body = body.replace("AI monitoring and drilling systems, autonomous underwater drones", "automated drilling diagnostics alongside self-navigating subsea drones")

# 5. Check if any "Ultra-Deepwater vs Ultra-Large Vessels" heading overlap exists
# In original title: "Ultra-Deepwater vs. Ultra-Large Vessels: Ocean Depth or Trade Scale?"

draft['body'] = body

with open('/opt/hermes/profiles/archie/rewrite_draft.json', 'w') as f:
    json.dump(draft, f, indent=2)

print("Refinement applied successfully.")
