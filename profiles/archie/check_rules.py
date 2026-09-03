import re
import sys

def check_article(text, meta_title, meta_desc):
    issues = []
    
    # Rule 1: Zero em-dashes
    if '—' in text or '–' in text or ' -- ' in text:
        issues.append("Rule 1 Violation: Em-dash or en-dash detected.")
        
    # Rule 4: No explicit transitional connectors
    forbidden_connectors = [
        r'\bFurthermore\b', r'\bMoreover\b', r'\bIn addition\b', 
        r'\bThat\'s why\b', r'\bIt is important to note\b', r'\bAdditionally\b',
        r'\bConsequently\b', r'\bTherefore\b', r'\bThus\b'
    ]
    for conn in forbidden_connectors:
        if re.search(conn, text, re.IGNORECASE):
            issues.append(f"Rule 4 Violation: Found forbidden connector '{conn}'.")

    # Rule 5: Contrastive negation limit (not X, but Y / instead of)
    negations = re.findall(r'\bnot\b.*?\bbut\b|\binstead of\b|\brather than\b', text, re.IGNORECASE)
    if len(negations) > 1:
        issues.append(f"Rule 5 Violation: Found {len(negations)} contrastive negations (max 1 allowed): {negations}")
        
    # Rule 6: Limit aphoristic isolated sentences (single-sentence paragraphs)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    for i, p in enumerate(paragraphs):
        # Skip markdown headings
        lines = p.split('\n')
        non_header_lines = [l for l in lines if not l.strip().startswith('#') and not l.strip().startswith('-') and not l.strip().startswith('*')]
        if not non_header_lines:
            continue
        body_text = ' '.join(non_header_lines)
        # count sentences roughly
        sentences = [s for s in re.split(r'[.!?]+', body_text) if s.strip()]
        if len(sentences) == 1:
            issues.append(f"Rule 6 Violation: Paragraph {i+1} has only 1 sentence: '{body_text}'")

    # Rule 9: Meta length limits
    if len(meta_title) > 60:
        issues.append(f"Rule 9 Violation: Meta Title length is {len(meta_title)} (> 60 chars).")
    if len(meta_desc) > 155:
        issues.append(f"Rule 9 Violation: Meta Description length is {len(meta_desc)} (> 155 chars).")

    # Check AI markers / fluff
    ai_words = ['delve', 'tapestry', 'beacon', 'paramount', 'testament', 'pivotal', 'fostering', 'game-changer', 'nestled', 'seamlessly', 'vital role', 'crucial aspect', 'in today\'s world', 'in today\'s fast-paced world']
    for word in ai_words:
        if re.search(r'\b' + word + r'\b', text, re.IGNORECASE):
            issues.append(f"AI Word Warning: Found '{word}' in text.")

    # Check source entity retention
    if 'Audio Visual Nation' not in text:
        issues.append("Rule 11 Violation: Missing 'Audio Visual Nation'")
    if 'Long Beach' not in text:
        issues.append("Rule 11 Violation: Missing 'Long Beach'")
    if 'SeaRates' not in text:
        issues.append("Rule 11 Violation: Missing 'SeaRates'")

    return issues

if __name__ == '__main__':
    print("Updated checker script ready.")
