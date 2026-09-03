# Test script to verify constraints
import re

def check_rules(title, meta_title, meta_desc, body):
    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"
    
    # Rule 1: No em-dashes
    if "—" in full_text or "--" in full_text:
        print("FAIL: Em-dash found!")
    else:
        print("PASS: No em-dashes.")

    # Rule 2: AI Cliches
    cliches = [
        "today's fast-paced world", "delve into", "delve", "plays a crucial role", 
        "game-changer", "game changer", "seamless integration", "testament to", 
        "important to note", "tapestry", "landscape", "beacon", "cutting-edge",
        "revolutionize", "ever-evolving", "furthermore", "moreover"
    ]
    found_cliches = [c for c in cliches if c in full_text.lower()]
    if found_cliches:
        print(f"FAIL: Found cliches: {found_cliches}")
    else:
        print("PASS: No AI cliches found.")

    # Rule 6: Explicit connectors
    connectors = ["that's why", "which is why", "that's a sign of", "thats why", "which is why"]
    found_conn = [c for c in connectors if c in full_text.lower()]
    if found_conn:
        print(f"FAIL: Found connectors: {found_conn}")
    else:
        print("PASS: No explicit connectors found.")

    # Rule 7: Contrastive negation limit
    # Count "not" vs "instead of" etc.
    negations = re.findall(r'\b(instead of|\b\w+\s*,\s*not\b)', full_text.lower())
    print(f"INFO: Contrastive negations detected: {negations}")

    # Check lengths
    print(f"Title len: {len(title)} (Max 60)")
    print(f"Meta-Title len: {len(meta_title)} (Max 60)")
    print(f"Meta-Description len: {len(meta_desc)} (Max 155)")

if __name__ == "__main__":
    t = "First Zero-Click AI Freight Booking on SeaRates"
    mt = "First Zero-Click AI Freight Booking on SeaRates"
    md = "On July 22, 2025, a shipper booked freight from Shanghai to Hamburg using an OpenAI MCP agent on SeaRates without clicking a mouse."
    b = "Sample body text"
    check_rules(t, mt, md, b)
