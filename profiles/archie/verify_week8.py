import json
import re

title = "SeaRates Week 8 Updates: Terminal API, Carrier Tracking"
meta_title = "SeaRates 2025 Week 8: Terminal API and Carrier Tracking"
meta_description = "SeaRates launches Terminal API v1.0, adds 3 carriers for multi-carrier tracking, updates ocean freight visibility tools, and refines ship schedules."

body_text = """SeaRates released several platform updates in Week 8 of 2025 across terminal data, vessel tracking, sailing schedules, and booking management.

Terminal API integration reached Version 1.0, opening access to data across more than 17,000 facilities indexed by SMDG and BIC codes. The update adds support for CONTAINER TERMINAL ODESSA (CTO) alongside BROOKLYN-KIEV PORT (BKP). Raw status responses now return specific facility flags. These include UNKNOWN, ON_TERMINAL, NOT_ON_TERMINAL, TERMINAL_NOT_SUPPORTED, TERMINAL_NO_RESPONSE, plus UNEXPECTED_ERROR. Standardizing these codes gives logistics teams cleaner container status tracking during terminal handoffs.

Multi-carrier tracking expanded to 191 supported ocean lines. GS Lines and Bahri (Saudi Arabia) joined the platform, alongside Vuxx Shipping. Data connections were also refined across fifteen established shipping lines. Ocean freight visibility improves through updated carrier feeds from Gold Star Line, Crane Worldwide Logistics, Dong Young, White Line Shipping, Hede Shipping, Dole Ocean Cargo Express, Matson Navigation, Aladin Express, Namsung Shipping, Maersk, Mediterranean Shipping Company (MSC), CMA CGM, American President Lines (APL), CNC (Cheng Lie Navigation), and Australia National Line (ANL).

Ship Schedules logic was updated for query results by Points across five providers: ONE, Hapag-Lloyd, Wan Hai, Yang Ming, and Sinotrans. Separately, booking management interfaces now display route details organized by shipment type and delivery mode within the Details tab."""

# Verification checks
output_data = {
    "Title": title,
    "Meta-Title": meta_title,
    "Meta-Description": meta_description,
    "Body Text": body_text
}

# 1. Max length checks
title_len = len(title)
meta_title_len = len(meta_title)
meta_desc_len = len(meta_description)

print(f"Title ({title_len}/60): {title}")
print(f"Meta-Title ({meta_title_len}/60): {meta_title}")
print(f"Meta-Description ({meta_desc_len}/155): {meta_description}")

assert title_len <= 60, "Title exceeds 60 chars"
assert meta_title_len <= 60, "Meta-Title exceeds 60 chars"
assert meta_desc_len <= 155, "Meta-Description exceeds 155 chars"

# 2. Em-dash check
full_text = f"{title}\n{meta_title}\n{meta_description}\n{body_text}"
em_dashes = re.findall(r'—|–|--', full_text)
print(f"Em-dashes count: {len(em_dashes)}")
assert len(em_dashes) == 0, f"Found em-dashes: {em_dashes}"

# 3. Slop / clichés check
slop_list = [
    "important to note", "fast-paced world", "delve into", "testament to", 
    "unlock", "seamless", "game-changer", "pivotal", "in conclusion"
]
for slop in slop_list:
    assert slop not in full_text.lower(), f"Found AI slop: {slop}"

# 4. Connectors check
connectors = ["that's why", "which is why", "this is why"]
for conn in connectors:
    assert conn not in full_text.lower(), f"Found connector: {conn}"

# 5. Contrastive negation check
contrastive_count = full_text.lower().count("instead of") + full_text.lower().count(" rather than ")
print(f"Contrastive negations count: {contrastive_count}")
assert contrastive_count <= 1, "Too many contrastive negations"

# 6. Keywords check
keywords = [
    "Terminal API integration",
    "SMDG and BIC codes",
    "Container status tracking",
    "Ocean freight visibility",
    "Multi-carrier tracking"
]
for kw in keywords:
    assert kw.lower() in full_text.lower(), f"Missing keyword: {kw}"

print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")
