import re

title = "SeaRates Updates: Week 32, 2025 Logistics Tracking"
meta_title = "SeaRates Updates | Week 32, 2025 Release Notes"
meta_desc = "Explore SeaRates Week 32 updates: expanded multi-carrier tracking, CONCOR rail support, automated transit time calculation, and CRM booking sync."

body = """We pushed a fresh set of updates across SeaRates in Week 32 of 2025. This release expands our coverage across ocean, air, and rail carriers while refining tools across our digital logistics workspace.

For multi-carrier container tracking, SACO Shipping Line joins our network as carrier number 210. Alongside this addition, we refreshed data connections for 12 existing ocean carriers: M-Line, Emirates Shipping Line, Ocean Network Express (ONE), TransContainer, SM Line (SML), COSCO, Mediterranean Shipping Company (MSC), Asyad Line, CMA CGM, Akkon Lines, Pacific International Lines (PIL), and Wan Hai. These updates maintain real-time shipment visibility across key trade routes.

Our multimodal freight tracking now covers more ground in the air and on tracks. We added Corendon Airlines and Surinam Airways to Air Tracking, bringing total supported airlines to 445. Integrations for Malaysia Airlines, Air Incheon, ASL Airlines Belgium, Air New Zealand, Finnair, Singapore Airlines, and Lufthansa Cargo were also updated. On rail, Container Corporation of India (CONCOR) becomes our 5th supported rail carrier.

Ship Schedules got a boost through updated carrier collaboration with Dongjin Shipping, SallaumLines, and Wallenius Wilhelmsen by Points. We also expanded the vessel database, adding 352 vessels operated by 19 worldwide shipping lines.

Inside the Rate Management System (RMS), automated transit time calculation is now active when adding or editing sea rates. The system determines transit times automatically using route parameters and shipping line data. Elsewhere in the platform, Route Planner now features a dedicated Pricing page, DFA Membership has a new landing page, and the Booking System syncs data directly with CRM records. On the Logistics Map, we updated the visual design for Cargoes and Transport displays.

Work is underway on several upcoming releases:
* Unified Tracking System
* Logistics Map 'Warehouse' tab
* Load Calculator Web 3.0 (new design and features)
* Map Platform
* AI Assistant integrated with Ship Schedules
* Geocoding API integrated with Logistics Explorer
* Inbox integration with Logistics Explorer, Bookings, and Notifications"""

full_content = f"1. Title: {title}\n2. Meta-Title: {meta_title}\n3. Meta-Description: {meta_desc}\n\n4. Full Body Text:\n{body}"

print("=== CHECKING RULES ===")

# Rule 1: Em-Dashes
dashes = re.findall(r'—|--|\s+-\s+', full_content)
print(f"Rule 1 (No Em-Dashes): {len(dashes)} found")

# Rule 2: AI Clichés
banned_phrases = [
    "glad to present", "excited to announce", "seamless", "delighted", "pleased to introduce",
    "in today's world", "it's not just", "game-changer", "testament", "cutting-edge",
    "robust", "dive in", "fostering", "elevate", "unlock", "empower", "strive to",
    "look no further", "without further ado", "continued support", "make your work easier"
]
found = [p for p in banned_phrases if p.lower() in full_content.lower()]
print(f"Rule 2 (No AI Clichés): {found if found else 'PASSED'}")

# Rule 6: Connectors
connectors = ["that's why", "which is why", "this means that", "because of this", "in order to"]
found_conn = [c for c in connectors if c.lower() in full_content.lower()]
print(f"Rule 6 (No Over-Explaining Connectors): {found_conn if found_conn else 'PASSED'}")

# Rule 7: Contrastive Negation
negations = re.findall(r'\b(not\s+[^,.]+,\s*but|isn\'t\s+[^,.]+,\s*it\'s|is not\s+[^,.]+,\s*it is)\b', full_content, re.IGNORECASE)
print(f"Rule 7 (Contrastive Negation <= 1): {len(negations)} found")

# Fact Grounding Check
facts = [
    "SACO Shipping Line", "210", "M-Line", "Emirates Shipping Line", "Ocean Network Express (ONE)",
    "TransContainer", "SM Line (SML)", "COSCO", "Mediterranean Shipping Company (MSC)", "Asyad Line",
    "CMA CGM", "Akkon Lines", "Pacific International Lines (PIL)", "Wan Hai",
    "Corendon Airlines", "Surinam Airways", "445", "Malaysia Airlines", "Air Incheon",
    "ASL Airlines Belgium", "Air New Zealand", "Finnair", "Singapore Airlines", "Lufthansa Cargo",
    "Container Corporation of India (CONCOR)", "5", "Dongjin Shipping", "SallaumLines",
    "Wallenius Wilhelmsen by Points", "352 vessels", "19 worldwide shipping lines",
    "Pricing page", "Route Planner", "DFA Membership", "Booking System", "CRM",
    "RMS", "transit time", "sea rates", "Logistics Map", "Cargoes and Transport",
    "Unified Tracking System", "Logistics Map 'Warehouse' tab", "Load Calculator Web 3.0",
    "Map Platform", "AI Assistant", "Geocoding API", "Inbox integration"
]

missing_facts = [f for f in facts if f.lower() not in full_content.lower()]
print(f"Fact Grounding Check: Missing facts: {missing_facts if missing_facts else 'NONE - ALL FACTS GROUNDED'}")

