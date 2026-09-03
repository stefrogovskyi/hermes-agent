import re

rewritten_body = """TITLE: Temporary Fencing in Freight Yards and Shipping Ports
META TITLE: Temporary Fencing in Freight Yards and Shipping Ports
META DESCRIPTION: Use modular fencing for port perimeter security, cargo theft deterrence, and ISPS facility compliance across active freight yards.

BODY:
A port perimeter is never static. Freight yards move billions in electronics, automotive parts, medical supplies, and luxury goods around the clock, with trucks, cranes, and containers in continuous motion. Huge open grounds make permanent walls impractical for every operational shift. When expansion projects, temporary storage setups, or rerouted traffic flows open sudden gaps, unauthorized entry, equipment loss, and cargo theft follow quickly. Unmanaged traffic leads directly to breaches, property damage, and severe delays.

### Perimeter Gaps in Active Logistics Operations
Logistics sites face constant motion. Heavy machinery and haulers move continuously alongside public access corridors, worker zones, and visiting drivers. Certain yards even sit near areas accessible to tourists or inspectors.

When high-value loads sit in holding zones or loading docks without dedicated barriers, opportunistic thieves take advantage. Basic barriers force intruders to deal with an extra physical barrier, buying crucial time for security teams to intercept them. Rapid deployment without heavy groundwork keeps operations moving while establishing strong visual deterrence.

### Deploying Modular Barriers Across High-Risk Zones
Installing modular security fencing creates immediate visual and physical boundaries around vulnerable areas. Manufacturers like Fortawall design these modular systems to reconfigure on short notice, adjusting whenever yard layouts shift daily.

During active expansion projects, port perimeter security depends on separating construction hazards from routine freight movements. Fencing off work zones keeps the public, delivery crews, and port personnel away from heavy equipment while isolating construction from daily vessel and yard workflows.

### Funneling Movement and Access
Managing gates and fencing lines gives managers precise freight yard access control. Directing drivers, workers, inspectors, and visitors through designated checkpoints simplifies credential checks and tightens accountability. Structured foot traffic and vehicle lanes keep crowded yards from descending into operational confusion. Controlled entry points are essential when facilities handle bonded inventory, customs-cleared goods, or hazardous materials.

For short-term site changes, modular barriers offer a flexible, cost-effective alternative to permanent installations. They support ISPS facility compliance by maintaining mandatory security standards under the International Ship and Port Facility Security Code without forcing costly civil engineering work.

### Operational Protocols and Integration
To maximize cargo theft deterrence, site operators should follow key setup and maintenance protocols:

- **Anti-climb panels:** Select panel designs that prevent easy handholds.
- **Base anchoring:** Secure panels using heavy bases or ground anchors to prevent tipping under wind or impact.
- **System integration:** Tie fence lines directly into lighting, motion sensors, and AI-powered surveillance systems.
- **Inspection routines:** Conduct regular physical inspections to catch loose clamps or damaged frames early.
- **Staff training:** Train terminal personnel thoroughly on gate protocols and access procedures."""

# Layer B checks:
em_dashes = len(re.findall(r'—', rewritten_body))
double_hyphens = len(re.findall(r'--', rewritten_body))

ai_words = [
    'delve', 'testament', 'vital role', 'crucial role', 'crucial', 'seamless', 'seamlessly',
    'game-changer', 'game changer', 'landscape', 'tapestry', 'fostering', 'foster', 'harnessing',
    'harness', 'in order to', 'serves as', 'ever-evolving', 'ever evolving', 'cutting-edge', 'cutting edge',
    'realm', 'transformative', 'mastering', 'revolutionize', 'beacon', 'pivotal', 'unprecedented',
    'elevate', 'paramount', 'vital', 'essential', 'strategic', 'durable', 'robust', 'foster', 'intertwined',
    'synergy', 'holistic', 'multifaceted', 'cornerstone', 'beacon'
]

found_ai_words = []
for word in ai_words:
    matches = re.findall(r'\b' + re.escape(word) + r'\b', rewritten_body, re.IGNORECASE)
    if matches:
        found_ai_words.append((word, len(matches)))

print("LAYER B FINDINGS:")
print(f"Em-dashes count: {em_dashes}")
print(f"Double hyphens count: {double_hyphens}")
print("AI clichés / buzzwords found:")
for w, c in found_ai_words:
    print(f"  - '{w}': {c}")

# Layer C checks:
# Connectors opening sentences
connectors = [
    'Furthermore', 'Moreover', 'In addition', 'Additionally', 'Consequently', 'Therefore',
    'Thus', 'Hence', 'That\'s why', 'Which is why', 'In conclusion', 'To conclude', 'In summary',
    'Overall', 'As a result', 'Ultimately'
]
found_connectors = []
for conn in connectors:
    matches = re.findall(r'^\s*' + re.escape(conn) + r'\b', rewritten_body, re.IGNORECASE | re.MULTILINE)
    if matches:
        found_connectors.append((conn, len(matches)))

print("\nLAYER C FINDINGS:")
print("Sentence-opening connectors found:")
for conn, c in found_connectors:
    print(f"  - '{conn}': {c}")

# Contrastive negation
# Patterns: "not X, but Y", "not only X, but Y", "X, not Y", "instead of X", "rather than"
negation_patterns = [
    r'\bnot\b.*?\bbut\b',
    r'\binstead of\b',
    r'\brather than\b',
    r'\bnot just\b',
    r'\bnot only\b'
]
found_negations = []
for pat in negation_patterns:
    m = re.findall(pat, rewritten_body, re.IGNORECASE)
    if m:
        found_negations.extend(m)

print(f"Contrastive negations / comparative structures found ({len(found_negations)}):")
for n in found_negations:
    print(f"  - '{n}'")

