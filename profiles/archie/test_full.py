import re

content = """TITLE: SeaRates at TPM25 in Long Beach
META_TITLE: Meet SeaRates at TPM25 in Long Beach
META_DESCRIPTION: SeaRates attends S&P Global TPM25 in Long Beach, March 2-5, 2025. Connect with our team on digital shipping. Email sales@searates.com.

BODY:
Four days in March, ocean freight gathers where Long Beach meets the Pacific. SeaRates representatives will be on site for TPM25 by S&P Global from March 2 to 5, 2025, at the Long Beach Convention Center. We are booking face-to-face meetings for clients and partners throughout the event.

Track options span Container Shipping, the TPM25 CEO Series, TPM Tech, Intermodal Rail, TPM Cold Chain, Trucking and Inland Distribution, Trade Policy, the TPM25 Academy, Networking, and Shipper Case Studies. Speakers, startups, investors, and industry leaders will tackle operational freight topics. Presentations cover 2025 container shipping prospects, post-covid trends, theoretical sessions, smart container deployment, and air cargo efficiency. Cold chain panels address market analysis, shipper-carrier relations, and the Move to -15C Coalition for refrigerated shippers. AI logistics guides, regulatory compliance solutions, supply chain stability, decarbonization power, and tech accessibility for shippers sit alongside geopolitical policy discussions on Trump's tariffs for Mexico, Asia, and Europe. Detailed schedules for the first two days are available on the TPM25 website.

Our team will answer shipping queries and discuss ways to improve the digital side of your logistics and trading operations. To schedule a time with SeaRates staff or request details regarding upcoming conferences, write to sales@searates.com.
"""

def verify_all(text):
    print("=== RULE 1: EM-DASH / EN-DASH CHECK ===")
    dashes = re.findall(r'—|--|–', text)
    print(f"Dashes found: {len(dashes)}")
    assert len(dashes) == 0

    print("\n=== LENGTH CHECKS ===")
    lines = text.strip().split('\n')
    for l in lines:
        if l.startswith("TITLE:"):
            t = l.replace("TITLE:", "").strip()
            print(f"TITLE len: {len(t)} (max 60)")
            assert len(t) <= 60
        elif l.startswith("META_TITLE:"):
            mt = l.replace("META_TITLE:", "").strip()
            print(f"META_TITLE len: {len(mt)} (max 60)")
            assert len(mt) <= 60
        elif l.startswith("META_DESCRIPTION:"):
            md = l.replace("META_DESCRIPTION:", "").strip()
            print(f"META_DESCRIPTION len: {len(md)} (max 155)")
            assert len(md) <= 155

    print("\n=== RULE 2: AI CLICHÉS CHECK ===")
    cliches = [
        "important to note", "crucial role", "delve into", "vital role", 
        "in today's world", "testament to", "unwavering commitment", 
        "game-changer", "dive into", "tapestry", "beacon", "landscape", 
        "foster", "unlock", "harness", "spearhead", "navigate", "realm",
        "pivotal", "boasts", "rich", "seamless", "ever-evolving", "strive",
        "furthermore", "moreover", "in conclusion", "to summarize",
        "mutually beneficial", "opportunity of a lifetime", "fruitful",
        "cutting-edge", "valuable advice"
    ]
    found = [c for c in cliches if c in text.lower()]
    print(f"AI Clichés found: {found}")
    assert len(found) == 0

    print("\n=== RULE 6: OVER-EXPLAINING CONNECTORS ===")
    connectors = ["that's why", "which is why", "that's a sign of", "this means that", "as a result of this"]
    found_conn = [c for c in connectors if c in text.lower()]
    print(f"Connectors found: {found_conn}")
    assert len(found_conn) == 0

    print("\n=== RULE 7: CONTRASTIVE NEGATION ('X, not Y', 'instead of') ===")
    cn = re.findall(r'\b(instead of|rather than|not\s+\w+\s+but)\b', text, re.IGNORECASE)
    cn_comma = re.findall(r',\s*not\b', text, re.IGNORECASE)
    all_cn = cn + cn_comma
    print(f"Contrastive negations count: {len(all_cn)} ({all_cn})")
    assert len(all_cn) <= 1

    print("\n=== SENTENCE LENGTHS & BURSTINESS ===")
    body_part = text.split("BODY:\n")[1]
    paragraphs = [p.strip() for p in body_part.split("\n\n") if p.strip()]
    
    for i, p in enumerate(paragraphs):
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
        lens = [len(s.split()) for s in sents]
        print(f"P{i+1} ({len(sents)} sentences): word counts = {lens}")
        print(f"   Opening: \"{sents[0]}\"")
        print(f"   Ending: \"{sents[-1]}\"")

verify_all(content)
