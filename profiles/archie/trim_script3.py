import re

with open("/opt/hermes/profiles/archie/draft_article.md", "r") as f:
    text = f.read()

subtle_trims = [
    ("When customs authorities place a hold on a container, the shipment sits in the terminal while officials request corrected documentation or conduct physical cargo inspections.", "When customs authorities place a hold on a container, the shipment sits in the terminal while officials request corrected documentation or conduct physical inspections."),
    ("Discrepancies between Bills of Lading and commercial invoices can invalidate insurance coverage. If cargo suffers damage during transit or port handling, adjusters review all shipping records.", "Discrepancies between Bills of Lading and commercial invoices can invalidate insurance coverage. If cargo suffers damage, adjusters review all shipping records."),
    ("Poor last-mile drayage coordination happens when shippers treat vessel estimated arrival dates as fixed constants rather than moving targets.", "Poor drayage coordination happens when shippers treat vessel arrival dates as fixed constants rather than moving targets."),
    ("Moisture damage presents another major hazard inside steel shipping containers during long ocean voyages. Ambient temperature changes cause water vapor inside the sealed container to condense on cold walls and ceiling surfaces, dripping onto cargo.", "Moisture damage presents another major hazard inside steel shipping containers during ocean voyages. Ambient temperature changes cause water vapor inside sealed containers to condense on cold walls and ceilings, dripping onto cargo."),
    ("An automotive parts distributor shipped exclusively with one carrier alliance along a single trade route. When severe weather caused a series of port blank sailings, the carrier suspended bookings for three weeks.", "An automotive parts distributor shipped exclusively with one carrier alliance. When severe weather caused port blank sailings, the carrier suspended bookings for three weeks.")
]

for old, new in subtle_trims:
    text = text.replace(old, new)

with open("/opt/hermes/profiles/archie/draft_article.md", "w") as f:
    f.write(text)

print("Trimmed to target ~1,730 words.")
