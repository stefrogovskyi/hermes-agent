# Complete Audit Verification Script

def run_audit():
    print("=== LAYER A AUDIT ===")
    # 6-gram matches
    # Raw 6-grams total = 43 matching 6-gram sliding windows
    # Grouped into contiguous block matches:
    # 1) "all searates tools and api integrations" (6 words)
    # 2) "akkon lines hecny shipping yang ming dole ocean cargo express carpenters shipping stolt tank containers stc cosiarma s p a ck line namsung shipping dong young shipping and lucky logistics air tracking" (32 words) -> Allowed Proper Noun List exception (carrier names).
    # 3) "parcel tracking api statistics world sea ports api statistics" (9 words) -> Proper Noun / UI label exception.
    # 4) "freight index api and access statistics" (6 words) -> Proper Noun / UI label exception.
    # 5) "transport and facilities management panels booking" (6 words) -> Proper Noun / UI panel exception.
    # 6) "new design and features map platform geocoding api integrated with logistics explorer inbox integration" (14 words) -> Contains verbatim phrasing "new design and features", "geocoding api integrated with logistics explorer".

    print("=== LAYER B AUDIT ===")
    # Em-dashes: 0
    # Double-dashes: 0
    # AI Cliches: 0

    print("=== LAYER C AUDIT ===")
    # Connectors forbidden: 0
    # Contrastive negations: 0 (limit <= 1)
    # Paragraph variance: Good word count variation (18 to 55 words)
    # Monotonous lists: Standard bullet lists
    # Bow-tie wrap-ups: 0
    # Twin sentence patterns: None

    print("=== LAYER D AUDIT ===")
    # Factual errors / distortions:
    # 1. "Improved collaboration with shipping lines" -> rewritten as "Integration logic has also been upgraded across ocean lines" (Invented technical mechanism / API code refactoring).
    # 2. "Updated support for airlines in API" -> rewritten as "updated data structures for Malaysia Airlines..." (Invented technical detail / data structure changes).
    # 3. "Announcements:" -> rewritten as "## Upcoming Features" + "Development continues on several tools scheduled for release:" (Invented status / wrongly classifying announcements as future/unreleased tools under development).

run_audit()
