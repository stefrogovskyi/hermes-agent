import re

title = "SeaRates Week 5 Updates: Tracking API & Schedules"
meta_title = "SeaRates Week 5 Updates | Container & Air Tracking API"
meta_desc = "SeaRates Week 5, 2025 updates: added Kanway and Sidra lines, updated air cargo tracking integration, vessel schedules, and logistics rate tools."

body = """Moving goods across borders relies on raw data moving just as fast.

SeaRates released several platform updates during the fifth week of 2025. These changes focus on tracking capabilities, schedules, and developer resources.

Container and Ocean Freight Updates
The SeaRates real-time container tracking API now includes support for Kanway Line and Sidra Line. This addition brings the total number of supported ocean carriers to 182. Along with expanded carrier coverage, the system features improved carrier auto-detection logic for shipping lines, assisting with vessel schedule auto-detection.

SeaRates also updated data integrations for five shipping lines and leasing companies:
- Econship
- Tailwind Shipping Lines
- Seatrade
- Emirates Shipping Line
- DSV Ocean Transport

Air Cargo and Schedules
Air cargo tracking integration received performance updates across eight airlines:
- China Southern Airlines
- Juneyao Airlines
- Delta Air Lines
- China Cargo Airlines
- EVA Air
- Challenge Airlines
- ANA Cargo
- Malaysia Airlines

These changes deliver more accurate and timely tracking information for air shipments.

For sea freight planning, vessel schedule support was updated for Swire Shipping, Evergreen, Econship, Kambara Kisen, Eukor, Sinotrans, and KMTC by Points.

Developer Tools and Site Pages
Geocoding API output data results were improved. SeaRates also published new dedicated landing pages for the Individual Quotes API and the Search Filter feature. 

Finally, content was refreshed for two core logistics rate management tools: the Freight Index and the Carbon Emissions Calculator. Together, these updates deliver broader multimodal freight visibility for daily supply chain operations."""

print(f"Title ({len(title)} chars): {title}")
print(f"Meta-Title ({len(meta_title)} chars): {meta_title}")
print(f"Meta-Description ({len(meta_desc)} chars): {meta_desc}")

keywords = [
    "real-time container tracking API",
    "multimodal freight visibility",
    "air cargo tracking integration",
    "vessel schedule auto-detection",
    "logistics rate management tools"
]

all_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

# Rule 1 Check
has_emdash = '—' in all_text or '--' in all_text
print("Rule 1 (No em-dashes):", "FAIL" if has_emdash else "PASS")

# Rule 2 Check
cliches = [
    "crucial", "testament", "delve", "in today's world", "game-changer",
    "vital role", "beacon", "seamless", "landscape", "paradigm", "realm",
    "ever-evolving", "cutting-edge", "fostering", "empower", "transformative",
    "unlocking", "comprehensive", "boast", "bolster", "revolution", "spearhead",
    "pivotal", "cornerstone", "game changer"
]
found_cliches = [c for c in cliches if c.lower() in all_text.lower()]
print("Rule 2 (No AI clichés):", f"FAIL: {found_cliches}" if found_cliches else "PASS")

# Target Keywords Check
for kw in keywords:
    print(f"Keyword '{kw}':", "PASS" if kw.lower() in all_text.lower() else "FAIL")

# Rule 6 Check
bridges = ["that's why", "which is why", "that's a sign of", "this means that"]
found_bridges = [b for b in bridges if b.lower() in all_text.lower()]
print("Rule 6 (No connectors):", f"FAIL: {found_bridges}" if found_bridges else "PASS")

# Rule 7 Check
cn_1 = re.findall(r'\binstead of\b', all_text, re.IGNORECASE)
cn_2 = re.findall(r',\s*not\s+', all_text, re.IGNORECASE)
print(f"Rule 7 (Contrastive negations): {len(cn_1) + len(cn_2)} (max 1)")

