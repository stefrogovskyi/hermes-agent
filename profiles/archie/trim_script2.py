import re

with open("/opt/hermes/profiles/archie/draft_article.md", "r") as f:
    text = f.read()

subtle_trims = [
    ("Managing ocean cargo requires structured planning, precise documentation, and proactive tracking across every transit leg. Shippers can eliminate these expenses by addressing five specific operational traps.", "Managing ocean cargo requires structured planning, precise documentation, and proactive tracking across every leg. Shippers can eliminate these expenses by addressing five operational traps."),
    ("Effective ocean freight risk mitigation requires embedding maritime transport into a rolling supply strategy rather than treating ocean carriers as short-notice backup providers.", "Effective ocean freight risk mitigation requires embedding maritime transport into a rolling supply strategy rather than treating carriers as short-notice backup providers."),
    ("A chemical distributor imported liquid additives using outdated six-digit HS codes on the customs entry that did not match destination tariff classifications.", "A chemical distributor imported liquid additives using outdated six-digit HS codes that did not match destination tariff classifications."),
    ("An electronics exporter packed forty-foot containers manually without calculating volume distribution, leaving fifteen percent of usable cubic space empty while placing heavy power units on one side.", "An electronics exporter packed containers manually without calculating volume distribution, leaving fifteen percent of cubic space empty while placing heavy power units on one side."),
    ("Maintaining multi-carrier contracts and utilizing digital rate tools allows logistics teams to pivot shipments quickly to open routes without paying extreme spot premiums.", "Maintaining multi-carrier contracts and utilizing digital rate tools allows logistics teams to pivot shipments quickly without paying extreme spot premiums.")
]

for old, new in subtle_trims:
    text = text.replace(old, new)

with open("/opt/hermes/profiles/archie/draft_article.md", "w") as f:
    f.write(text)

print("Trimmed slightly.")
