import json
import re

title = "TILOG LOGISTIX 2024: SeaRates in Bangkok"
meta_title = "TILOG LOGISTIX 2024: SeaRates at BITEC"
meta_description = "SeaRates joined 9,000+ attendees and 415 brands at TILOG LOGISTIX 2024 in Bangkok to showcase digital freight tools."

body_markdown = """Bangkok hosted TILOG LOGISTIX 2024 from August 15 to 17 at the BITEC exhibition center. Over three days, 415 technology and service provider brands from 25 countries set up alongside more than 9,000 entrepreneurs and operators.

### Inside the BITEC Halls

SeaRates Account Manager Kate Borkut represented the team at the event. She met with international attendees in group conference sessions and one-on-one meetings, presenting the SeaRates marketplace and digital community. Professionals across material handling, packaging, warehousing, and IT examined upcoming supply chain trends for 2024 and 2025.

### Focus Areas and Field Discussions

Talks centered on practical ways to apply digital logistics tools, raise supply chain efficiency, and integrate IT solutions into daily freight management. Global business leaders and product developers gathered around one clear target: operational efficiency.

SeaRates supports over one million users across the globe with software for shipment tracking, freight optimization, and general logistics management. Direct questions or partnership inquiries to sales@searates.com."""

# Check metadata lengths
assert len(title) <= 60, f"Title too long: {len(title)}"
assert len(meta_title) <= 60, f"Meta Title too long: {len(meta_title)}"
assert len(meta_description) <= 155, f"Meta Description too long: {len(meta_description)}"

# Check Rule 1: No em-dashes or en-dashes or double hyphens anywhere
full_text = f"{title}\n{meta_title}\n{meta_description}\n{body_markdown}"

dashes = ["—", "–", "--"]
for d in dashes:
    assert d not in full_text, f"Found dash '{d}' in text"

# Check Rule 10 & 4: Forbidden words / AI clichés / connectors
cliches_and_connectors = [
    "delve", "testament", "crucial", "seamless", "landscape", "tapestry", "beacon",
    "pivotal", "transformative", "fostering", "game-changer", "realm", "ever-evolving",
    "unlock", "harness", "vibrant", "synergy", "underscore", "spearhead", "trailblazer",
    "furthermore", "moreover", "in conclusion", "additionally", "in summary", "overall",
    "consequently", "thus", "therefore", "besides"
]

full_text_lower = full_text.lower()
for word in cliches_and_connectors:
    pattern = r'\b' + re.escape(word) + r'\b'
    assert not re.search(pattern, full_text_lower), f"Found forbidden word/connector: '{word}'"

print("All automated checks PASSED!")
print("Title length:", len(title))
print("Meta title length:", len(meta_title))
print("Meta description length:", len(meta_description))

output_json = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_description,
    "body_markdown": body_markdown
}

print("\n--- JSON OUTPUT ---")
print(json.dumps(output_json, indent=2))

