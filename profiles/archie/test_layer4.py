# Let's list all facts and compare:

facts_comparison = [
    ("Week 8", "Week 8", "Matches"),
    ("Year not stated", "Year 2025 inserted", "Assumed year (2025) added in title/body"),
    ("17,000+ terminals", "more than 17,000 facilities", "Matches"),
    ("SMDG and BIC codes", "SMDG and BIC codes", "Matches"),
    ("CONTAINER TERMINAL ODESSA (CTO)", "CONTAINER TERMINAL ODESSA (CTO)", "Matches"),
    ("BROOKLYN-KIEV PORT (BKP)", "BROOKLYN-KIEV PORT (BKP)", "Matches"),
    ("container statuses: UNKNOWN, ON_TERMINAL, NOT_ON_TERMINAL, TERMINAL_NOT_SUPPORTED, TERMINAL_NO_RESPONSE, UNEXPECTED_ERROR",
     "facility flags: UNKNOWN, ON_TERMINAL, NOT_ON_TERMINAL, TERMINAL_NOT_SUPPORTED, TERMINAL_NO_RESPONSE, plus UNEXPECTED_ERROR",
     "Described as 'facility flags' instead of 'container statuses'"),
    ("3 more shipping lines (GS Lines, Bahri, Vuxx Shipping)", "GS Lines, Bahri, Vuxx Shipping added", "Matches"),
    ("Total shipping lines: 191", "191 supported ocean lines", "Matches"),
    ("15 enhanced shipping lines listed", "fifteen established shipping lines", "Matches count (15)"),
    ("Ship Schedules providers by Points: ONE, Hapag-Lloyd, Wan Hai, Yang Ming, Sinotrans", "five providers by Points", "Matches count (5)"),
    ("Bookings: route displaying by shipment and delivery type under 'Details' tab",
     "booking management interfaces: route details organized by shipment type and delivery mode within Details tab",
     "Matches (delivery type -> delivery mode)")
]

for orig, draft_v, notes in facts_comparison:
    print(f"ORIGINAL: {orig}\nDRAFT: {draft_v}\nNOTES: {notes}\n{'-'*50}")
