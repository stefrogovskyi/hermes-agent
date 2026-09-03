import json
import re

text_data = {
    "title": "SeaRates at LISW25: Key Learnings from London International Shipping Week",
    "meta_title": "SeaRates at LISW25: London International Shipping Week Recap",
    "meta_description": "SeaRates recap from LISW25 at IMO Headquarters in London, covering maritime decarbonization, S-100 standards, and end-to-end supply chain visibility.",
    "content": """During the week of September 15 through 19, 2025, SeaRates participated in London International Shipping Week (LISW25) at the IMO Headquarters in London. The event focused on the central theme of The Management of Paradox in Global Shipping, addressing trade-offs between growth, emissions reduction, vessel speed, safety, regulation, and technical innovation.

The week opened officially at the London Stock Exchange and covered key tracks including maritime decarbonization, digital transformation, supply chain resilience, and regulatory compliance. On September 16, DNV presented its Maritime Forecast to 2050 at IET London. The UKHO also hosted its "S-100 in focus" panel, examining new navigation and mapping standards. The S-100 hydrographic e-navigation standard is central to digital ecosystems, vessel safety, and standardized port operations.

Throughout the week, we met with clients, carriers, and technology partners to demonstrate how SeaRates tools assist with daily operations. We presented our rate calculation and tracking tools, real-time freight calculation, container and air cargo tracking, CO2 emissions analytics, and custom IT solutions designed for supply chain transparency and cost control.

Four operational realities stood out during the week. First, decarbonization is shifting from strategy to direct implementation, with operations moving from basic energy efficiency steps to alternative fuel pilots under the supervision of regulators and financial institutions.

Second, data functions as a shared language across maritime digital transformation. Standards like S-100 establish common protocols for shared navigation and digital port services. Companies that invest in data normalization and open integrations secure advantages in speed and security.

Third, cargo owners and 3PLs are requiring end-to-end supply chain visibility, risk forecasting, and route replanning to maintain resilient logistics networks.

Finally, skills shortages and new safety rules are driving investments in crew support, training, and human-in-the-loop digital processes rather than total automation.

We thank the LISW25 organizers and the IMO for bringing industry leaders together to address global shipping challenges. To discuss custom logistics solutions or LISW25 topics, contact our team at it.sales@searates.com or connect directly with our representatives, Kateryna Komarova or Lilia Khovrak."""
}

full_str = json.dumps(text_data, indent=2)

# Check Rule 1: Zero Em-Dashes
em_dash_matches = re.findall(r'—|--| - ', full_str)
assert len(em_dash_matches) == 0, f"Em-dashes found: {em_dash_matches}"

# Check Rule 2: No AI Clichés / Slop
clichés = [
    "delve", "in today's world", "testament", "pivotal", "game-changer", 
    "vital role", "it's not just", "in conclusion", "furthermore", "moreover", 
    "leverage", "tapestry", "beacon", "fostering", "seamlessly", "realm", 
    "spearhead", "holistic", "landscape", "paramount", "catalyst", "paradigm", "cornerstone"
]
found_clichés = [c for c in clichés if c.lower() in full_str.lower()]
assert len(found_clichés) == 0, f"Clichés found: {found_clichés}"

# Check Rule 5: No Over-explaining Connectors
connectors = ["that's why", "which is why", "this is why", "that's a sign of"]
found_connectors = [conn for conn in connectors if conn.lower() in full_str.lower()]
assert len(found_connectors) == 0, f"Connectors found: {found_connectors}"

# Check Rule 6: Strict Contrastive Negation Limit (Max 1)
negation_patterns = [
    r'\brather than\b',
    r'\binstead of\b',
    r'\bnot\b.*?\bbut\b',
    r', not\b'
]
contrastive_matches = []
for p in negation_patterns:
    m = re.findall(p, full_str, re.IGNORECASE)
    if m:
        contrastive_matches.extend(m)
print("Contrastive negations:", len(contrastive_matches), contrastive_matches)
assert len(contrastive_matches) <= 1, f"Too many contrastive negations: {contrastive_matches}"

# Check Keywords
keywords = [
    "maritime decarbonization",
    "S-100 hydrographic e-navigation standard",
    "end-to-end supply chain visibility",
    "maritime digital transformation",
    "rate calculation and tracking tools"
]
for kw in keywords:
    assert kw.lower() in full_str.lower(), f"Missing keyword: {kw}"

# Check valid JSON
obj = json.loads(full_str)
print("ALL TESTS PASSED SUCCESSFULLY!")
