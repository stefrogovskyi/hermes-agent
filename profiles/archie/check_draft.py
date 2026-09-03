import json
import re

audit_phrases = [
    "supplier acquisition and selection based on beneficial terms",
    "inventory planning and optimization, warehouse operations control",
    "planning and supplies regulation",
    "instant access to extended analytics",
    "inbound and outbound logistics operations in a few clicks",
    "warehouse operators port authorities production managers",
    "inventory levels without shortages or overstocks"
]

cliche_words = [
    "streamlines", "streamline", "streamlining",
    "heightens", "heighten",
    "interconnected",
    "coordinated",
    "vital",
    "elevate", "elevates",
    "comprehensive",
    "tailored",
    "optimize", "optimizes", "optimized", "optimizing", "optimization"
]

transition_words = [
    "furthermore", "in addition", "moreover", "that's why", "therefore", "consequently",
    "additionally", "however", "nonetheless", "nevertheless", "besides"
]

def check_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    body = data.get("body_markdown", "")
    meta_desc = data.get("meta_description", "")
    full_text = json.dumps(data).lower()
    
    print(f"Meta description length: {len(meta_desc)}")
    if len(meta_desc) > 155:
        print("WARNING: Meta description > 155 chars!")
        
    # Check em-dashes
    em_dashes = body.count("—") + body.count("--") # check for actual em dashes
    print(f"Em-dashes count: {body.count('—')}")
    
    # Check cliché words
    found_cliches = []
    for word in cliche_words:
        # word boundary search
        matches = re.findall(rf'\b{re.escape(word)}\b', full_text, re.IGNORECASE)
        if matches:
            found_cliches.append((word, len(matches)))
    print(f"Cliche words found: {found_cliches}")
    
    # Check transitions
    found_transitions = []
    for tw in transition_words:
        matches = re.findall(rf'\b{re.escape(tw)}\b', full_text, re.IGNORECASE)
        if matches:
            found_transitions.append((tw, len(matches)))
    print(f"Transitions found: {found_transitions}")

    # Check 6-word verbatim matches with original text/audit phrases
    for phrase in audit_phrases:
        if phrase.lower() in full_text:
            print(f"WARNING: Audit phrase matched: '{phrase}'")

    # Check H4 headings
    if "####" in body:
        print("WARNING: Found H4 headings!")
        
    # Check sentence starters with -ing verbs
    sentences = re.split(r'[.!?]\s+', body)
    ing_starters = [s for s in sentences if re.match(r'^\s*[*#-]*\s*[A-Z][a-z]+ing\b', s)]
    print(f"Sentence starting with -ing verbs count: {len(ing_starters)}")
    for s in ing_starters:
        print(f"  - {s[:50]}...")

if __name__ == "__main__":
    check_json("candidate.json")
