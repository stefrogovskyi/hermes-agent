import json
import re

payload = {
  "title": "Managing Counterparties in SeaRates Virtual Office",
  "meta_title": "Counterparties Panel in SeaRates Virtual Office",
  "meta_description": "Organize customers, leads, partners, and carriers in SeaRates Virtual Office. Import XLS files, filter records, and generate invitation links.",
  "body_markdown": """Managing commercial connections across freight forwarding, shipping, and supply chain operations often breaks down when contact details sit scattered across loose spreadsheets or separate communication apps. Within the SeaRates Virtual Office, the Counterparties panel brings these contact details together into a single system, providing clear visibility and central management for daily trade activities. Users holding Vendor or Carrier account types can access this tool directly from their workspace.

To open the workspace, start from the SeaRates home page and head to your Profile in the Virtual Office. On the left main menu, locate the Activity section and select the Counterparties tab. Adding a contact begins with clicking the Add counterparty button, which opens a quick data form. Here, you enter basic contact parameters including email, first name, last name, phone number, and country. You then assign the entry to a specific category: Customer, Lead, Partner, Colleague, Vendor, Carrier, or Other.

Once created, your records appear in a structured directory where you can edit, duplicate, or delete entries at any time. When working with high volumes of data, such as bringing in bulk supplier lists, row view options can be set to 10, 25, 50, or 100 rows per page. Built in XLS import and export features allow teams to upload existing data files or back up records with minimal manual entry.

For contacts who do not have an active platform membership, the interface includes a feature to generate an individual invitation link to join SeaRates. Locating specific profile information remains straightforward through dedicated filter controls. Clicking on header fields such as Company, Type, Name, Email, Country, or Creation date lets you filter the list using suggested choices.

By gathering stakeholder information into one central hub, businesses can replace bulky spreadsheets with an organized Virtual Office workspace. The Counterparties panel helps maintain clean records for every trade partner while keeping routine administrative tasks manageable. To learn more about setting up Virtual Office tools for your business operations, reach out to sales@searates.com."""
}

def verify_all(data):
    title = data["title"]
    meta_title = data["meta_title"]
    meta_desc = data["meta_description"]
    body = data["body_markdown"]
    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

    print("--- CHARACTER LENGTH CHECKS ---")
    print(f"Title length: {len(title)} (max 60) -> {'PASS' if len(title) <= 60 else 'FAIL'}")
    print(f"Meta Title length: {len(meta_title)} (max 60) -> {'PASS' if len(meta_title) <= 60 else 'FAIL'}")
    print(f"Meta Desc length: {len(meta_desc)} (max 155) -> {'PASS' if len(meta_desc) <= 155 else 'FAIL'}")

    print("\n--- RULE 1: DASHES CHECK ---")
    dashes = ["—", "–", "--"]
    dash_found = False
    for d in dashes:
        if d in full_text:
            print(f"FAIL: Dash '{d}' found!")
            dash_found = True
    if not dash_found:
        print("PASS: No forbidden dashes found.")

    print("\n--- RULE 2: BANNED AI CLICHES CHECK ---")
    banned_phrases = [
        "delve into", "testament to", "crucial role", "vital role", "in today's fast-paced world",
        "it is worth noting", "game-changer", "seamless", "seamlessly", "landscape", "tapestry",
        "beacon", "pivotal", "spearheading", "unlocking", "realm", "harness", "empower",
        "vibrant", "fostering", "elevate", "cutting-edge", "let's explore", "in conclusion"
    ]
    cliche_found = False
    for phrase in banned_phrases:
        if re.search(r'\b' + re.escape(phrase) + r'\b', full_text, re.IGNORECASE):
            print(f"FAIL: Banned AI cliché found: '{phrase}'")
            cliche_found = True
    if not cliche_found:
        print("PASS: No banned AI clichés found.")

    print("\n--- RULE 5: CONTRASTIVE NEGATION CHECK ---")
    contrastive_indicators = ["instead of", "rather than", ", not ", "not X but Y"]
    neg_count = 0
    for ind in contrastive_indicators:
        matches = re.findall(re.escape(ind), full_text, re.IGNORECASE)
        neg_count += len(matches)
    print(f"Contrastive negation count: {neg_count} (max 1) -> {'PASS' if neg_count <= 1 else 'FAIL'}")

    print("\n--- RULE 6: APHORISTIC ONE-LINER CHECK ---")
    paragraphs = [p.strip() for p in body.split("\n\n") if p.strip()]
    one_liners = 0
    for p in paragraphs:
        # split by sentence endings
        sentences = [s for s in re.split(r'[.!?]\s+', p) if s]
        if len(sentences) == 1:
            one_liners += 1
            print(f"Single sentence paragraph found: {p}")
    print(f"One-liner paragraphs count: {one_liners} (max 1-2) -> {'PASS' if one_liners <= 2 else 'FAIL'}")

    print("\n--- RULE 8: EXPLICIT CONNECTORS CHECK ---")
    banned_openers = ["Furthermore", "Moreover", "In addition", "Consequently", "That said", "That's why"]
    opener_found = False
    sentences = re.split(r'[.!?]\s+', body)
    for s in sentences:
        s_strip = s.strip()
        for opener in banned_openers:
            if s_strip.startswith(opener):
                print(f"FAIL: Banned opener found: '{opener}' in '{s_strip}'")
                opener_found = True
    if not opener_found:
        print("PASS: No forbidden sentence openers found.")

verify_all(payload)
