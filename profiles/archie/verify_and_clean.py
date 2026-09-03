import re

title = "SeaRates Week 51 Updates 2024: New APIs & Tracking"
meta_title = "SeaRates Week 51 Updates 2024: New APIs and Tracking"
meta_description = "SeaRates week 51 updates 2024 introduce Dole Ocean Cargo Express container tracking, dry port freight rate calculator tools, and new Developer Portal APIs."

body = """## Container and Air Cargo Tracking Upgrades

The SeaRates tracking system now includes Dole Ocean Cargo Express container tracking, raising the total number of supported ocean shipping lines to 180. Tracking integrations have been updated for several ocean carriers, including Crowley Maritime, W.E.C. (West European Container) Lines, Avana Global FZCO (BALAJI), COSCO, and Wan Hai.

Air freight tracking capabilities have been updated for SriLankan Airlines and El Al Israel Airlines.

## Demurrage & Storage Calculator API and Rate Calculation Tools

Developers can now access the official Demurrage Storage Calculator API. Complete integration documentation is available in the logistics API Developer Portal. For web users, the processing queue for demurrage and detention calculations has been updated, ensuring improved processing of calculation data results.

Logistics Explorer now includes a dry port freight rate calculator autocomplete feature. Shippers can select dry port inland hubs directly when searching for freight estimates. Ship Schedules received updates, introducing support for Ignazio Messina by Port. Processing logic has been updated for Ignazio Messina by Points, ZIM by Points, Sinotrans by Port, and T.S Lines by Vessel.

## Developer Portal Integrations and Platform Features

A web-integrated version of Request a Quote is now available. Platform owners can fetch the integration code from the Developer Portal to place quote request forms directly on their sites. An updated list of API response status codes and descriptions has been added to the Developer Portal.

Virtual Office management for counterparties has been updated. Invite link generation now detects where the link is created, using either the SeaRates.com domain or the custom domain of the platform owner. Interface updates include redesigned header and profile menus on LandRates.com and a new Vendors page on AirRates.com.

## Product Roadmap and Announcements

SeaRates is preparing several upcoming releases across web and mobile products:

* New Version of Route Planner API
* Freight Index 1.0
* Mobile App Version 1.2 featuring an integrated Request System
* Load Calculator Version 2.2
* Map platform"""

def verify_all():
    errors = []
    full_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"
    
    # 1. Check lengths
    if len(title) > 60:
        errors.append(f"Title length {len(title)} > 60")
    if len(meta_title) > 60:
        errors.append(f"Meta Title length {len(meta_title)} > 60")
    if len(meta_description) > 155:
        errors.append(f"Meta Description length {len(meta_description)} > 155")
        
    # 2. Check em-dashes
    for dash in ["—", "–", "--"]:
        if dash in full_text:
            errors.append(f"Found dash '{dash}'")
    if re.search(r'\s+-\s+', full_text):
        errors.append("Found space-hyphen-space acting as em-dash")
        
    # 3. Check AI clichés
    cliches = [
        "important to note", "delve into", "in today's world", "testament to", 
        "game-changer", "key aspect", "not just", "in conclusion", "furthermore", 
        "moreover", "seamless", "robust", "leverage", "revolutionize", "tapestry",
        "beacon", "landscape", "unlock", "elevate", "cutting-edge", "game changer",
        "excited to announce", "pleased to announce", "thrilled"
    ]
    for c in cliches:
        if c in full_text.lower():
            errors.append(f"AI cliché found: '{c}'")

    # 4. Check over-explaining connectors & cause-effect phrasing
    connectors = [
        "that's why", "which is why", "that's a sign of", "this is why", 
        "this means that", "this ensures that", "this ensures",
        "to help developers troubleshoot", "cutting down processing delays",
        "decrease status retrieval errors", "deliver more precise milestone"
    ]
    for conn in connectors:
        if conn in full_text.lower():
            errors.append(f"Forbidden connector / cause-effect phrase found: '{conn}'")

    # 5. Contrastive negation check
    negation_patterns = [
        r'\bnot\b.*?\binstead\b',
        r'\binstead of\b',
        r',\s*not\b',
        r"isn't\b.*?\bit's\b",
        r"is not\b.*?\bit is\b"
    ]
    for pat in negation_patterns:
        if re.search(pat, full_text, re.IGNORECASE):
            errors.append(f"Contrastive negation found with pattern: {pat}")

    print("Verification complete.")
    if errors:
        print("ERRORS FOUND:")
        for e in errors:
            print(" -", e)
    else:
        print("ALL CHECKS PASSED PERFECTLY!")

    print(f"\nLengths:\nTitle: {len(title)}\nMeta Title: {len(meta_title)}\nMeta Description: {len(meta_description)}")

if __name__ == "__main__":
    verify_all()
