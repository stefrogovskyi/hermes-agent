import json
import re

result = {
    "title": "SeaRates Headed to VDS 2024 in Valencia",
    "meta_title": "SeaRates at VDS 2024 in Valencia: Connect With Our Team",
    "meta_description": "Meet SeaRates and Olexandr Grabarchuk at VDS 2024 in Valencia on Oct 23-24 to discuss shipping and logistics solutions. Contact sales@searates.com.",
    "body_md": """The SeaRates team is attending VDS 2024 on October 23-24, hosted at the City of Arts and Sciences in Valencia, Spain. The gathering brings together representatives from international startups, global corporations, and institutional investors. Centered on this year's theme, 'Embracing Evolution: Invest in the Leaders of Tomorrow', discussions will focus on how modern technological advancements shape logistics, trade, and broader industry sectors.

## Industry Leaders Gather in Valencia

VDS 2024 expects 12,000+ attendees, 600+ speakers, 700+ investors, and 2,500+ startups from across the world. Presentations and discussions will span eight dedicated spaces across the venue: the Main, Santander, Green, Audiovisual, Discovery, and Pitch Stages, alongside the Workshop Room & VIP Boxes.

The two-day conference program covers several key areas:
* Practical AI adoption for global businesses, sustainable investment strategies, and resilient supply chain formation
* Startup ecosystem growth, pitch competitions, and presentation sessions
* Joint innovation initiatives linking tech developers with port operations
* Regional investment analysis highlighting opportunities across South America and Europe
* Collaborative funding frameworks between maritime entrepreneurs and public agencies
* Scalable financial technologies tailored for international commerce
* Emerging workplace trends, including social transformation and business mental health initiatives

Detailed schedule information for both days is available on the official VDS website. Attendees can review session times and speaker lineups prior to arriving in Valencia.

## Meet Olexandr Grabarchuk at the Event

Olexandr Grabarchuk will represent SeaRates on site throughout the two-day event. Our team is available to meet with clients, partners, and industry peers to exchange insights on freight movement and digital trade tools. Whether you want to streamline cargo operations or evaluate digital tools for your freight requirements, we welcome the opportunity to connect in person.

To arrange a dedicated meeting with our team during VDS 2024 or learn more about our upcoming event appearances, send an email to sales@searates.com. We look forward to meeting you in Valencia this October."""
}

# Verification script
errors = []

# Rule 1: EM-DASH BAN
for key in ["title", "meta_title", "meta_description", "body_md"]:
    text = result[key]
    if "—" in text or "–" in text or "--" in text:
        errors.append(f"Em-dash or forbidden dash found in {key}")

# Rule 10: Metadata constraints
if len(result["meta_title"]) > 60:
    errors.append(f"meta_title length ({len(result['meta_title'])}) > 60")
if len(result["meta_description"]) > 155:
    errors.append(f"meta_description length ({len(result['meta_description'])}) > 155")

# Rule 4: Forbidden connectors
forbidden_connectors = [
    r"\bfurthermore\b", r"\bin addition\b", r"\bmoreover\b", r"\bconsequently\b",
    r"\bhowever\b", r"\bin summary\b", r"\boverall\b", r"\bit is worth noting\b",
    r"\badditionally\b", r"\bas a result\b", r"\btherefore\b", r"\bin conclusion\b",
    r"\bcrucially\b", r"\bimportantly\b"
]
for conn in forbidden_connectors:
    if re.search(conn, result["body_md"], re.IGNORECASE):
        errors.append(f"Forbidden connector found: {conn}")

# Rule 3: Textbook headings
textbook_headings = ["introduction", "key takeaways", "conclusion", "conference agenda", "summary", "overview"]
for h in textbook_headings:
    if h in result["body_md"].lower():
        errors.append(f"Textbook heading found: {h}")

# Rule 9: Check exact required facts
required_facts = [
    "VDS 2024", "Valencia", "City of Arts and Sciences", "October 23-24",
    "12,000+", "600+", "700+", "2,500+", "Main", "Santander", "Green", "Audiovisual",
    "Discovery", "Pitch", "Workshop Room & VIP Boxes", "Embracing Evolution: Invest in the Leaders of Tomorrow",
    "South America", "Europe", "Olexandr Grabarchuk", "sales@searates.com"
]

for fact in required_facts:
    if fact not in result["body_md"] and fact not in result["meta_description"]:
        errors.append(f"Missing required fact: {fact}")

# Check JSON validity
try:
    json_str = json.dumps(result)
    json.loads(json_str)
except Exception as e:
    errors.append(f"JSON error: {e}")

print("ERRORS:", errors if errors else "NONE")
print("meta_title length:", len(result["meta_title"]))
print("meta_description length:", len(result["meta_description"]))
