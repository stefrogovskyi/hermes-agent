import re

def check_text(title, meta_title, meta_desc, body):
    errors = []
    
    # Rule 1: No em-dashes or double hyphens
    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"
    if "—" in full_text or "\u2014" in full_text:
        errors.append("EM-DASH FOUND!")
    if "--" in full_text:
        errors.append("DOUBLE HYPHEN FOUND!")
    if "–" in full_text or "\u2013" in full_text:
        errors.append("EN-DASH FOUND!")
        
    # Title lengths
    if len(title) > 60:
        errors.append(f"Title too long: {len(title)} > 60")
    if len(meta_title) > 60:
        errors.append(f"Meta title too long: {len(meta_title)} > 60")
    if len(meta_desc) > 155:
        errors.append(f"Meta description too long: {len(meta_desc)} > 155")
        
    # Keywords
    keywords = [
        "real-time freight tracking API",
        "multimodal supply chain visibility",
        "AIS vessel tracking data",
        "DB Schenker road tracking",
        "container tracking API",
        "carbon emissions route mapping"
    ]
    for kw in keywords:
        if kw.lower() not in full_text.lower():
            errors.append(f"Missing keyword: {kw}")
            
    # Connectors forbidden
    forbidden_connectors = ["that's why", "which is why", "that's a sign of", "in this article", "in conclusion"]
    for fc in forbidden_connectors:
        if fc in full_text.lower():
            errors.append(f"Forbidden connector/phrase found: {fc}")
            
    # Source facts check
    required_facts = [
        "DB Schenker", "cargo_units", "sections", "Nhava Sheva Freeport Terminal",
        "OOCL", "COSCO", "Hapag-Lloyd", "Maersk",
        "Cathay Pacific", "SpiceJet", "Singapore Airlines",
        "AirRates", "CO2 Calculator", "Ship Schedules", "Freight Index", "DFA Membership",
        "Unified Tracking System", "Logistics Map", "Load Calculator Web 3.0", "Map Platform", "Logistics Explorer"
    ]
    for fact in required_facts:
        if fact.lower() not in full_text.lower():
            errors.append(f"Missing source fact/entity: {fact}")

    print("ERRORS:", errors if errors else "NONE! ALL CHECKS PASSED.")

if __name__ == "__main__":
    print("Script ready")
