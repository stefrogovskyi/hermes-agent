from audit_script import original, candidate

# Let's inspect facts, counts, names, parameters in both texts.

# 1. Title/Meta
# Orig: "We add new features and make the site better every month, and this month is no different... If you sign up for our SeaRates news, we will let you know when there is a new update."
# Cand: "Title: SeaRates Development Release: August 2024 Updates"
# Cand: "Meta Title: SeaRates August 2024 Freight Platform Updates"
# Cand: "Meta Description: Discover SeaRates August 2024 updates..."
# Cand Body: "The August 2024 release..."
# Is "August 2024" in original?
print("Is 'August 2024' or 'August' in Original text?")
print("August in orig:", "August" in original)

# 2. Counts of Air Carriers
# Orig: "added support for 33 airlines:"
# Cand: "Integration coverage expanded to 33 additional air carriers:"
# Orig: "improved how we work with providers, including Kuwait Airways, Suparna Airlines, DHL Aviation, Air New Zealand, Cathay Pacific Airways, Saudi, Allied Air, El Al Israel Airlines, Batik Air, Qatar Airways, Delta Airlines, SouthWest Airlines, Atlas Air, Singapore Airlines, United Airlines, Finnair, Emirates, TAP Portugal, Air China Cargo, and Air India."
# Let's count provider list in Orig vs Cand:
orig_air_providers = ["Kuwait Airways", "Suparna Airlines", "DHL Aviation", "Air New Zealand", "Cathay Pacific Airways", "Saudi", "Allied Air", "El Al Israel Airlines", "Batik Air", "Qatar Airways", "Delta Airlines", "SouthWest Airlines", "Atlas Air", "Singapore Airlines", "United Airlines", "Finnair", "Emirates", "TAP Portugal", "Air China Cargo", "Air India"]
print("Orig air providers count:", len(orig_air_providers))
# Cand: "System processing improved across 20 existing air providers:"

# 3. Shipping lines / Ocean lines counts
# Orig: "Added support for 4 shipping lines: Safetrans Line, M-Line, Reel Shipping FZCO, and Hub Shipping."
# Cand: "Four shipping lines joined the Container Tracking network..."
# Orig ocean providers:
orig_ocean_providers = ["ECU Worldwide", "CMA CGM", "ZIM", "Yang Ming", "Avana Global FZCO (BALAJI)", "Evergreen", "W.E.C. (West European Container) Lines", "Hyundai Merchant Marine (HMM)", "Hapag-Lloyd", "Shipco Transport", "Orient Overseas Container Line (OOCL)", "Jin Jiang Shipping (SHJJ)", "Swire Shipping", "Atlantic Container Line (ACL)", "TransContainer", "Aladin Express", "NewStar", "Hellmann Worldwide Logistics", "Turkon", "Geodis Ocean", "Reel Shipping FZCO", "Sinokor", "Kuehne + Nagel (KN)", "Westwood Shipping Lines", "Hai Hua Shipping (HASCO)", "DHL Global Forwarding", "Dachser", "Emirates Shipping Line", "Meratus Line", "Pan Continental Shipping", "Ocean Network Express (ONE)", "COSCO"]
print("Orig ocean providers count:", len(orig_ocean_providers))
# Cand: "Carrier processing performance was upgraded for 33 providers:"
print("Cand says 33 providers for ocean lines.")

