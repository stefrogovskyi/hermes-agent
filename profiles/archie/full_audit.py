import re

rewrite_title = "Managing Counterparties in SeaRates Virtual Office"
rewrite_meta_title = "Counterparties Panel in SeaRates Virtual Office"
rewrite_meta_desc = "Organize customers, leads, partners, and carriers in SeaRates Virtual Office. Import XLS files, filter records, and generate invitation links."

rewrite_body = """Managing commercial connections across freight forwarding, shipping, and supply chain operations often breaks down when contact details sit scattered across loose spreadsheets or separate communication apps. Within the SeaRates Virtual Office, the Counterparties panel brings these contact details together into a single system, providing clear visibility and central management for daily trade activities. Users holding Vendor or Carrier account types can access this tool directly from their workspace.

To open the workspace, start from the SeaRates home page and head to your Profile in the Virtual Office. On the left main menu, locate the Activity section and select the Counterparties tab. Adding a contact begins with clicking the Add counterparty button, which opens a quick data form. Here, you enter basic contact parameters including email, first name, last name, phone number, and country. You then assign the entry to a specific category: Customer, Lead, Partner, Colleague, Vendor, Carrier, or Other.

Once created, your records appear in a structured directory where you can edit, duplicate, or delete entries at any time. When working with high volumes of data, such as bringing in bulk supplier lists, row view options can be set to 10, 25, 50, or 100 rows per page. Built in XLS import and export features allow teams to upload existing data files or back up records with minimal manual entry.

For contacts who do not have an active platform membership, the interface includes a feature to generate an individual invitation link to join SeaRates. Locating specific profile information remains straightforward through dedicated filter controls. Clicking on header fields such as Company, Type, Name, Email, Country, or Creation date lets you filter the list using suggested choices.

By gathering stakeholder information into one central hub, businesses can replace bulky spreadsheets with an organized Virtual Office workspace. The Counterparties panel helps maintain clean records for every trade partner while keeping routine administrative tasks manageable. To learn more about setting up Virtual Office tools for your business operations, reach out to sales@searates.com."""

full_rewrite = f"{rewrite_title}\n{rewrite_meta_title}\n{rewrite_meta_desc}\n{rewrite_body}"

# LAYER B
# 1. Dashes count
em_dashes = len(re.findall(r'—|--', full_rewrite))
en_dashes = len(re.findall(r'–', full_rewrite))
hyphens = len(re.findall(r'-', full_rewrite))

print("Layer B: Dashes:")
print(f"Em-dashes: {em_dashes}, En-dashes: {en_dashes}")

# 2. Clichés
cliche_list = [
    "delve into", "testament to", "crucial role", "vital role", "in today's world", 
    "game-changer", "game changer", "seamless", "landscape", "tapestry", "beacon", 
    "pivotal", "cutting-edge", "user-friendly", "streamline", "leverage", "robust",
    "empower", "unlock", "foster", "transformative", "revolutionize", "elevate",
    "delve", "testament", "pivotal role"
]

found_cliches = []
for c in cliche_list:
    if re.search(r'\b' + re.escape(c) + r'\b', full_rewrite, re.IGNORECASE):
        found_cliches.append(c)

print(f"Clichés found: {found_cliches}")


# LAYER C: Structure & Rhetorical Ticks
# 1. Sentence-opening connectors
# "Furthermore", "Moreover", "In addition", "That's why", "Additionally", "Besides", "Also", "Consequently", "Therefore", "Thus"
connectors = ["Furthermore", "Moreover", "In addition", "That's why", "Additionally", "Besides", "Consequently", "Therefore", "Thus"]

paragraphs = [p.strip() for p in rewrite_body.split('\n\n') if p.strip()]

sentences = []
for p_idx, p in enumerate(paragraphs):
    # split sentences
    raw_sents = re.split(r'(?<=[.!?])\s+', p)
    for s in raw_sents:
        sentences.append((p_idx, s.strip()))

found_connectors = []
for p_idx, s in sentences:
    first_word = s.split()[0].replace(',', '').replace(';', '') if s else ""
    first_two = " ".join(s.split()[:2]).replace(',', '') if len(s.split()) >= 2 else ""
    for conn in connectors:
        if s.lower().startswith(conn.lower()):
            found_connectors.append((s, conn))

print(f"Forbidden connector openers found: {found_connectors}")

# 2. Contrastive negations ("X, not Y", "instead of", "rather than", "not only", "not just")
negation_patterns = [
    r'\binstead of\b',
    r'\brather than\b',
    r',\s*not\b',
    r'\bnot only\b',
    r'\bnot just\b'
]

found_negations = []
for p_idx, s in sentences:
    for pat in negation_patterns:
        m = re.findall(pat, s, re.IGNORECASE)
        if m:
            found_negations.append((s, m))

print(f"Contrastive negations found: {len(found_negations)} -> {found_negations}")

# 3. Single-sentence paragraphs
single_sentence_paras = 0
for p_idx, p in enumerate(paragraphs):
    raw_sents = [s for s in re.split(r'(?<=[.!?])\s+', p) if s.strip()]
    print(f"Paragraph {p_idx+1} sentence count: {len(raw_sents)}")
    if len(raw_sents) == 1:
        single_sentence_paras += 1

print(f"Single-sentence paragraphs count: {single_sentence_paras}")

# 4. Check textbook architecture / section structures & parallel twin-sentences / symmetric antithesis pairs
print("\nSentence structure review:")
for i, (p_idx, s) in enumerate(sentences):
    print(f"P{p_idx+1} S{i+1}: {s}")

