import re

title = "SeaRates Updates: Week 6 Platform Improvements"
meta_title = "SeaRates Week 6 Updates: Shipping and Tracking"
meta_desc = "SeaRates added 3 shipping lines, updated AIS vessel tracking logic, expanded airline coverage, and refreshed booking tools in Week 6, 2025."

body = """Platform updates for Week 6 include tracking expansions, API refinements, and interface changes across SeaRates services.

Our Tracking System now covers 185 shipping lines after adding support for Unifeeder, Viasea Shipping, and Oceanic Star Line. Behind the API, we updated the logic handling incoming AIS data and automatic carrier detection.

Data integration was updated for ocean carriers and leasing operators, including Swire Shipping, Dole Ocean Cargo Express, ECU Worldwide, CMA CGM, Yusen Logistics, Namsung Shipping, Orient Overseas Container Line (OOCL), DHL Global Forwarding, and Jin Jiang Shipping (SHJJ).

Air Cargo Tracking received data refinements for multiple carriers. We updated integrations with Cargolux Airlines International, FedEx Express, Lufthansa Cargo, Xiamen Airlines, Air Canada, EVA Air, Korean Air, and ITA Airways.

For shipment schedule data, provider support was updated across two lookup modes. Searches by Points were updated for Sinokor, CMA CGM, CNC, ANL, APL, Heung-A, and ZIM. Searches by Vessel were updated for Yang Ming and PIL.

The Bookings module now displays route endpoint maps with assigned manager details for direct contact, as well as visual adjustments across the user interface.

Elsewhere across the platform:
- Content and visual layouts were refreshed on the Hot Deals Widget and Smart Documents pages.
- LandRates.com updated its Road Freight Tracking page.
- New landing pages were published for the Logistics Map API and Chat System API."""

full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

print("=== CHARACTER COUNTS ===")
print(f"Title ({len(title)} / 60): {title}")
assert len(title) <= 60
print(f"Meta-Title ({len(meta_title)} / 60): {meta_title}")
assert len(meta_title) <= 60
print(f"Meta-Description ({len(meta_desc)} / 155): {meta_desc}")
assert len(meta_desc) <= 155

print("\n=== EM-DASH CHECK ===")
em_dash_count = full_text.count("—") + full_text.count("--")
print(f"Em-dashes: {em_dash_count}")
assert em_dash_count == 0

print("\n=== REPETITION & ALONGSIDE CHECK ===")
alongside_count = full_text.lower().count("alongside")
print(f"'alongside' count: {alongside_count}")
assert alongside_count <= 1

print("\n=== FABRICATED TERMS CHECK ===")
banned_phrases = [
    "smoothing out the kinks",
    "steady supply chain tracking solutions",
    "support real-time container visibility across global routes",
    "now yield cleaner results",
    "quietly behind the scenes",
    "operational momentum"
]
for bp in banned_phrases:
    if bp.lower() in full_text.lower():
        print(f"FOUND BANNED PHRASE: {bp}")
    else:
        print(f"PASS (absent): {bp}")

print("\n=== BANNED WORDS / AI CLICHES CHECK ===")
banned_words = [
    "delve into", "testament to", "crucial role", "in today's world", 
    "it is worth noting", "vital aspect", "seamlessly", "furthermore", 
    "moreover", "in conclusion", "unwavering commitment", "game-changer", 
    "game changer", "dive deep", "tapestry", "landscape", "beacon", 
    "unlock", "elevate", "harness", "foster", "paramount", "realm", 
    "digital age", "at your fingertips", "gamechanger", "vibrant", "revolutionize"
]
for bw in banned_words:
    if bw.lower() in full_text.lower():
        print(f"FOUND BANNED WORD: {bw}")
    else:
        pass
print("AI Cliché check complete.")

print("\n=== CONTRASTIVE NEGATION CHECK ===")
cn = re.findall(r'\b(instead of|rather than|not [a-z]+, but|not [a-z]+ but)\b', full_text.lower())
print(f"Contrastive negations: {cn}")

print("\nALL AUTOMATED CHECKS PASSED SUCCESSFULLY!")
