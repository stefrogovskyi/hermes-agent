import re

draft_text = """Title: SeaRates Week 8 Updates: Terminal API, Carrier Tracking
Meta-Title: SeaRates 2025 Week 8: Terminal API and Carrier Tracking
Meta-Description: SeaRates launches Terminal API v1.0, adds 3 carriers for multi-carrier tracking, updates ocean freight visibility tools, and refines ship schedules.

Body Text:
SeaRates released several platform updates in Week 8 of 2025 across terminal data, vessel tracking, sailing schedules, and booking management.

Terminal API integration reached Version 1.0, opening access to data across more than 17,000 facilities indexed by SMDG and BIC codes. The update adds support for CONTAINER TERMINAL ODESSA (CTO) alongside BROOKLYN-KIEV PORT (BKP). Raw status responses now return specific facility flags. These include UNKNOWN, ON_TERMINAL, NOT_ON_TERMINAL, TERMINAL_NOT_SUPPORTED, TERMINAL_NO_RESPONSE, plus UNEXPECTED_ERROR. Standardizing these codes gives logistics teams cleaner container status tracking during terminal handoffs.

Multi-carrier tracking expanded to 191 supported ocean lines. GS Lines and Bahri (Saudi Arabia) joined the platform, alongside Vuxx Shipping. Data connections were also refined across fifteen established shipping lines. Ocean freight visibility improves through updated carrier feeds from Gold Star Line, Crane Worldwide Logistics, Dong Young, White Line Shipping, Hede Shipping, Dole Ocean Cargo Express, Matson Navigation, Aladin Express, Namsung Shipping, Maersk, Mediterranean Shipping Company (MSC), CMA CGM, American President Lines (APL), CNC (Cheng Lie Navigation), and Australia National Line (ANL).

Ship Schedules logic was updated for query results by Points across five providers: ONE, Hapag-Lloyd, Wan Hai, Yang Ming, and Sinotrans. Separately, booking management interfaces now display route details organized by shipment type and delivery mode within the Details tab."""

# Check for em-dashes
em_dashes = re.findall(r'—|–|--', draft_text)
print("Em-dashes count:", len(em_dashes), em_dashes)

# Common AI buzzwords check
buzzwords = [
    "delve", "testament", "beacon", "landscape", "pivotal", "boasts", "seamless", "seamlessly",
    "unlock", "harness", "elevate", "robust", "game-changer", "transformative", "crucial",
    "paramount", "fostering", "tapestry", "realm", "synergy", "spearhead", "overarching",
    "rich history", "ever-evolving", "nestled", "unwavering", "demystify", "unveil"
]

found_buzz = []
for b in buzzwords:
    matches = re.findall(r'\b' + b + r'\b', draft_text, re.IGNORECASE)
    if matches:
        found_buzz.append((b, len(matches)))

print("Buzzwords found:", found_buzz)

