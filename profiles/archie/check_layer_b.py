import re

title = "SeaRates Weekly Updates: Week 38, 2024"
meta_title = "SeaRates Week 38 Updates: Tracking & API Notes"
meta_desc = "SeaRates Week 38 updates: air cargo tracking, container tracking, historical freight index API, vessel ship schedules, and Apple account login."

body = """# SeaRates Weekly Updates: Week 38, 2024

Software improves when small details accumulate into reliable tools. In Week 38 of 2024, SeaRates deployed updates across tracking integrations, developer endpoints, and platform design.

Air cargo tracking now connects directly with five additional carriers: Cathay Pacific Airways, British Airways, Astral Aviation, Bringer Air Cargo Taxi Aereo, and EVA Air. Meanwhile, ocean container tracking expanded integrations for Orient Overseas Container Line (OOCL), Kuehne + Nagel (KN), and Volta Container Line.

API functionality received two targeted changes. The Freight Index now exposes historical indicative rates through both web and API channels. For proximity calculations, the distance & time API runs on updated logic to determine the closest location for every request.

Vessel ship schedules added tracking support for HR Lines and Great White Fleet, searchable by points, vessel, or port. Users navigating Logistics Explorer can now switch the tool interface to Spanish through new Spanish localization options.

Signing in is simpler with Apple account login and registration options. To finish the week's release, SeaRates updated the design and content on the About Us and Plans & Pricing pages."""

full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

# 1. Em-dash count
em_dash_em = full_text.count("—")
em_dash_double = full_text.count("--")
print("Em-dashes (—):", em_dash_em)
print("Em-dashes (--):", em_dash_double)

# 2. AI Clichés
cliches = [
    "seamless", "seamlessly", "game-changer", "game changer", "crucial", "delve", "delves", "delving",
    "testament", "landscape", "dynamic", "elevate", "elevates", "robust", "paramount", "foster",
    "fosters", "pivotal", "revolution", "revolutionary", "bespoke", "realm", "tailored", "beacon",
    "tapestry", "underscores", "underscore", "empower", "empowers", "unlock", "unlocks", "delightful",
    "thrilled", "passionate", "gratitude", "grateful", "cutting-edge", "gamechanger"
]

words_in_text = re.findall(r"\b\w+[\-\w]*\b", full_text.lower())

found_cliches = []
for c in cliches:
    if re.search(r'\b' + re.escape(c) + r'\b', full_text, re.IGNORECASE):
        found_cliches.append(c)

print("Found AI clichés:", found_cliches)
