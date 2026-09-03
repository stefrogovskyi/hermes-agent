import json
import re

title = "SeaRates Headed to VDS 2024 in Valencia"
meta_title = "SeaRates at VDS 2024 in Valencia: Connect With Our Team"
meta_description = "Meet SeaRates and Olexandr Grabarchuk at VDS 2024 in Valencia on Oct 23-24 to discuss shipping and logistics solutions. Contact sales@searates.com."

body_md = """The SeaRates team is attending VDS 2024 on October 23-24 at the City of Arts and Sciences in Valencia, Spain. The gathering brings together representatives from international startups, global corporations, and investors. Centered on this year's theme, 'Embracing Evolution: Invest in the Leaders of Tomorrow', discussions focus on how modern technological advancements shape logistics, trade, and industry sectors.

VDS 2024 brings together over 12,000 attendees, 600+ speakers, 700+ investors, and 2,500+ startups from across global industries. Presentations and discussions take place on the Main, Santander, Green, Audiovisual, Discovery, and Pitch Stages, as well as in the Workshop Room and VIP Boxes.

The two-day conference program covers several key areas:
* AI technologies for global businesses, covering collaboration, sustainable investment strategies, and supply chain formation
* Startup ecosystems, presentation sessions, and competitions
* Joint development opportunities for the innovation community and the port industry
* An overview of investment trends across global regions, such as South America and Europe
* Cooperation opportunities between public funding bodies and maritime entrepreneurship
* Scaling of financial technologies
* Social transformation and overcoming mental health challenges in business

For more information about the first- and second-day agenda, visit the VDS website.

Olexandr Grabarchuk will represent SeaRates on site throughout the two-day event. Our team is available to meet with clients, partners, and industry peers to exchange insights on shipping requirements and digital logistics solutions.

To learn more about SeaRates or get information about forthcoming conferences, contact sales@searates.com. We hope to see you in Valencia in October!"""

result_json = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_description,
    "body_md": body_md
}

print("JSON Output Valid:")
print(json.dumps(result_json, indent=2))

# 1. Length checks
print("\n--- Length Checks ---")
print(f"Title ({len(title)} <= 60): {len(title) <= 60}")
print(f"Meta Title ({len(meta_title)} <= 60): {len(meta_title) <= 60}")
print(f"Meta Description ({len(meta_description)} <= 155): {len(meta_description) <= 155}")

# 2. Dash checks
full_text = f"{title} {meta_title} {meta_description} {body_md}"
em_dashes = [c for c in full_text if c in ["—", "–"] or "--" in c]
print(f"\n--- Dash Check ---")
print(f"Em/En-dash count: {len(em_dashes)}")
for c in ["—", "–", "--"]:
    if c in full_text:
        print(f"FOUND PROHIBITED DASH: {repr(c)}")

# 3. AI Cliché checks
cliches = [
    "delve", "testament", "tapestry", "seamless", "seamlessly", "landscape", "pivotal",
    "fostering", "beacon", "realm", "vibrant", "nestled", "unlock", "harness", "elevate",
    "tailored", "resilient", "spearhead", "game-changer", "transformative", "crucial",
    "ever-evolving", "cutting-edge", "in conclusion", "in today's world", "vital asset",
    "important to note", "dive into"
]
found_cliches = []
for c in cliches:
    if re.search(r'\b' + re.escape(c) + r'\b', full_text, re.IGNORECASE):
        found_cliches.append(c)
print(f"\n--- AI Cliché Check ---")
print(f"Found clichés: {found_cliches}")

# 4. Connectors check
connectors = ["furthermore", "moreover", "in addition", "consequently", "however", "in summary", "overall", "it is worth noting", "that's why", "which is why"]
found_connectors = []
for c in connectors:
    if re.search(r'\b' + re.escape(c) + r'\b', full_text, re.IGNORECASE):
        found_connectors.append(c)
print(f"\n--- Connector Check ---")
print(f"Found connectors: {found_connectors}")

# 5. Headings check
headings = re.findall(r'^#+ .*', body_md, re.MULTILINE)
print(f"\n--- Markdown Headings Check ---")
print(f"Headings found: {headings}")

# 6. Audit terms check
print(f"\n--- Audit Specific Checks ---")
prohibited_phrases = [
    "eight dedicated spaces across the venue",
    "Attendees can review session times",
    "resilient supply chain formation",
    "financial technologies tailored for international commerce",
    "tech developers with port operations",
    "institutional investors",
    "emerging workplace trends"
]
for p in prohibited_phrases:
    if p.lower() in full_text.lower():
        print(f"FAIL: Found prohibited phrase: '{p}'")
    else:
        print(f"PASS: Not found: '{p}'")

required_phrases = [
    "Presentations and discussions take place on the Main, Santander, Green, Audiovisual, Discovery, and Pitch Stages, as well as in the Workshop Room and VIP Boxes.",
    "For more information about the first- and second-day agenda, visit the VDS website.",
    "To learn more about SeaRates or get information about forthcoming conferences, contact sales@searates.com.",
    "supply chain formation",
    "scaling of financial technologies",
    "the innovation community and the port industry",
    "social transformation and overcoming mental health challenges in business"
]
for r in required_phrases:
    if r.lower() in full_text.lower():
        print(f"PASS: Found required phrase: '{r}'")
    else:
        print(f"FAIL: Missing required phrase: '{r}'")

