import re

with open("/opt/hermes/profiles/archie/draft_article.md", "r") as f:
    text = f.read()

# Let's do subtle edits to tighten text
replacements = [
    ("giving shippers predictable costs and vast cargo capacity on primary trade routes.", "giving shippers predictable costs and high cargo capacity."),
    ("This reactive approach creates immediate operational vulnerability.", "This creates immediate operational risk."),
    ("Booking containers on short notice during peak shipping seasons leaves shippers exposed to elevated spot rates, congestion surcharges, and container rollings.", "Booking containers late leaves shippers exposed to elevated spot rates, congestion surcharges, and container rollings."),
    ("When vessels sail at full capacity, carriers prioritize contract cargo, pushing last-minute spot bookings onto subsequent sailings.", "When vessels sail full, carriers prioritize contract cargo, pushing spot bookings onto later sailings."),
    ("A rolled container delays shipments by two to three weeks, throwing production schedules into disarray.", "A rolled container delays shipments by weeks, disrupting production schedules."),
    ("Discrepancies between the Bill of Lading and commercial invoice can invalidate marine cargo insurance coverage.", "Discrepancies between Bills of Lading and commercial invoices can invalidate insurance coverage."),
    ("The transition from terminal discharge to inland drayage and warehouse receiving represents a vulnerable leg in the supply chain.", "The transition from terminal discharge to inland drayage represents a vulnerable supply chain leg."),
    ("Delaying container unloading at the warehouse incurs detention and chassis usage charges.", "Delaying warehouse unloading incurs detention and chassis fees."),
    ("Weather delays, port congestion, and berth availability shifts alter container availability windows with little notice.", "Weather, port congestion, and berth shifts alter container availability with little notice."),
    ("Overloaded or unbalanced containers fail Safety of Life at Sea (SOLAS) Verified Gross Mass (VGM) checks at port gates, resulting in turned-away trucks, re-weighing fees, and missed vessel cutoffs.", "Unbalanced containers fail SOLAS Verified Gross Mass (VGM) checks at port gates, causing turned-away trucks, re-weighing fees, and missed cutoffs."),
    ("Shippers relying on a single ocean carrier or single trade lane contract find themselves trapped with limited options when that carrier cancels sailings or skips port calls.", "Shippers relying on a single carrier contract find themselves trapped when sailings are canceled or ports skipped."),
    ("Eliminating these five sea freight traps transforms ocean shipping from an unpredictable expense into a disciplined supply chain advantage.", "Eliminating these five sea freight traps turns ocean shipping into a reliable supply chain advantage.")
]

for old, new in replacements:
    text = text.replace(old, new)

with open("/opt/hermes/profiles/archie/draft_article.md", "w") as f:
    f.write(text)

print("Updated text.")
