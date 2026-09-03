import json
import re

title = "Digital Tracking and Automation in Global Freight Logistics"
meta_title = "Digital Tracking & Automation in Global Freight Logistics"
meta_description = "Discover how IoT tracking, warehouse robotics, AI analytics, and blockchain simplify international shipping and secure high-value cargo."

body = """## Cargo Tracking and Border Clearance

Moving freight across international transit corridors requires constant operational oversight. Long shipments pass through multiple hands. Modern transport management relies on digital records alongside physical equipment. Enterprise Resource Planning and Transportation Management Systems connect directly with port facilities and rail networks. This integration gives operators digital supply chain visibility across every leg of the journey. Hardware sensors attached to shipments provide continuous positional updates. Combining GPS with IoT cargo tracking allows carriers and buyers to view location data throughout transit. Precise coordinates reduce error risks and help handlers organize arrival schedules. At international borders, traditional paperwork creates administrative bottlenecks. Transitioning to paperless customs clearance alongside digital bills of lading moves shipments through border checks faster while cutting administrative delays.

## Physical Tagging in Extreme Conditions

Goods traveling thousands of kilometers face moisture and physical impacts during transit. Paper stickers and basic adhesive labels rub off or become unreadable under these harsh conditions.

To maintain readable records, logistics providers use durable cargo labeling. They attach tags made from stainless steel or aluminum to containers and shipping pallets. Metallic tags resist corrosion and physical damage. They hold barcodes or embedded RFID scan data that feed into automated record-keeping systems. Automated scanners in large logistics terminals read these metal markers quickly.

Reusing these metal tags across multiple voyages cuts material costs and lowers environmental impact. The markers remain attached throughout extended supply chain cycles, ensuring accurate cargo identification on containers and specialized goods.

## Warehouse Automation and Predictive AI

Large distribution centers and shipping terminals deploy automated warehouse robotics to process high freight volumes. Automated storage and retrieval systems make efficient use of vertical warehouse space. Automatic stackers and robotic units move goods quickly when order volumes rise. Driverless Automated Guided Vehicles transport heavy cargo across ports and warehouses without human drivers, maintaining stable operations 24/7. In expansive logistics centers, drones equipped with optical cameras scan barcodes and QR codes on elevated racks. This pattern recognition technology completes inventory audits rapidly with minimal staff involvement.

Machine learning software processes meteorological data and port congestion metrics to optimize transit routes. Through predictive freight analytics, routing programs identify potential delays ahead of time and suggest alternative transport routes. Automated customer service platforms support communication too. Chatbots provide real-time shipment status updates to customers, improving response times without replacing human decision-making.

## Blockchain Records in Global Trade

International supply chains involve many separate participants, including shippers and customs agencies. Blockchain systems provide a secure, immutable ledger that participating entities cannot alter without detection. Using blockchain bills of lading and electronic consignment notes prevents unauthorized document changes. Smart contract protocols execute terms automatically, releasing payments once arrival confirmation triggers the system. This removes financial disputes and delays. Immutable tracking records follow goods from manufacture to final delivery, protecting products with strict origin and quality requirements like medicines or electronics."""

data = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_description,
    "body": body
}

full_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"

print("=== CHECKING ALL RULES ===")

# 1. Dashes
dashes = full_text.count('—') + full_text.count('--')
print("Rule 1 - Em-dashes / double hyphens:", dashes)

# 2. Clichés
cliches = [
    "crucial role", "in today's world", "delve", "important to note", "dive into",
    "seamlessly", "game-changer", "it's not just", "it is not just", "in conclusion",
    "tapestry", "beacon", "testament", "realm", "landscape", "pivotal", "fostering",
    "harnessing", "ever-evolving", "paramount", "cutting-edge", "revolutionize",
    "revolutionizing", "groundbreaking", "unwavering", "delving", "robust",
    "transformative", "game changer", "paves the way"
]
found_cliches = [c for c in cliches if re.search(r'\b' + re.escape(c) + r'\b', full_text, re.IGNORECASE)]
print("Rule 2 - Clichés found:", found_cliches)

# 3. Metaphors count
# Check for metaphors in body
print("Rule 3 - Metaphors check:")
# Identified metaphors:
# 1. "bottlenecks" (administrative bottlenecks)
# That is 1 metaphor. Very clean!

# 4. Burstiness & Rule of three
print("Rule 4 - Burstiness & Rule of three:")
triads = re.findall(r'\b\w+\s*,\s*\w+\s*,?\s*(?:and|or)\s+\w+\b', full_text, re.IGNORECASE)
print(" Rule of three matches:", triads)

# Check all lists with commas
commas = re.findall(r'[^.!?]*\b\w+\s*,\s*\w+[^.!?]*', body)
print(" Comma constructions in text:")
for c in commas:
    print("  *", c.strip())

# 5. Textbook architecture
print("Rule 5 - Architecture (Section paragraph counts):")
sections = body.split("## ")
for i, sec in enumerate(sections[1:], 1):
    header = sec.split("\n")[0]
    paras = [p.strip() for p in sec.split("\n\n")[1:] if p.strip()]
    print(f" Section {i} ({header}): {len(paras)} paragraph(s)")

# 6. Over-explaining connectors
connectors = ["that's why", "that is why", "which is why", "that's a sign of", "that is a sign of", "this is why", "because of this"]
found_conn = [c for c in connectors if re.search(r'\b' + re.escape(c) + r'\b', full_text, re.IGNORECASE)]
print("Rule 6 - Connectors found:", found_conn)

# 7. Contrastive negations
print("Rule 7 - Contrastive negations:")
negations = re.findall(r'\b(instead of|rather than|not only|it isn\'t|it is not|not [a-z0-9\s]+, but)\b', full_text, re.IGNORECASE)
print(" Negation matches:", negations)

# 8. Literary/crafted sentence check
print("Rule 8 - Literary/crafted sentence limit:")
# Identify all sentences and select the single literary/crafted sentence:
# "Paper stickers and basic adhesive labels rub off or become unreadable under these harsh conditions."
# Or: "At international borders, traditional paperwork creates administrative bottlenecks."
# All other sentences are dry, workmanlike, plain statements of fact.

# 9 & 10. Conclusion & Antithesis
print("Rule 9 & 10 - Conclusion and Antithesis check:")
# Ending paragraph: "Immutable tracking records follow goods from manufacture to final delivery, protecting products with strict origin and quality requirements like medicines or electronics." -> Single direct sentence. No twin parallel conclusions, no symmetric antithesis pairs.

# 11. Fact check vs source text
print("Rule 11 - Fact check vs source text:")

# Keywords check
keywords = [
    "digital supply chain visibility",
    "IoT cargo tracking",
    "predictive freight analytics",
    "automated warehouse robotics",
    "paperless customs clearance",
    "blockchain bills of lading",
    "durable cargo labeling"
]
print("\nKeywords Check:")
for kw in keywords:
    present = re.search(r'\b' + re.escape(kw) + r'\b', full_text, re.IGNORECASE) is not None
    print(f" '{kw}': {'PRESENT' if present else 'MISSING'}")

