import re

draft_text = """
Title: SeaRates December 2024 Release Notes: API Expansion and Platform Updates
Meta Title: SeaRates December 2024 Product Updates
Meta Description: SeaRates expanded carrier connections to 180, launched the Route Planner API, brought AWB tracking to mobile, and upgraded Virtual Office in December 2024.

Body Text:
SeaRates updated its core logistics tools and developer APIs in December 2024, expanding carrier tracking connections while introducing new route planning features.

### Container and Vessel Tracking
Ocean freight tracking now covers Cosco Specialized and Dole Ocean Cargo Express, bringing total supported carriers to 180. Users managing shipments on the container tracking web portal can view logistics milestones directly on a new Calendar tab. On the backend, the multi-carrier visibility API received updated location detection logic for precise event positioning.

Vessel schedule queries now accept Ignazio Messina and Pacific Forum Line by port. Users can also run schedule searches using alternative SCAC codes.

### Air Cargo Tracking
Air freight coverage grew to include four additional carriers: Aercaribe Peru, Air Cote D'Ivoire, Akasa Air, and Vensecar Internacional. Developers working with air cargo endpoints can review newly added status codes and response definitions in the Developer Portal.

Air freight visibility is also live on the SeaRates mobile app for iOS and Android. The mobile tool delivers real-time air freight AWB tracking with world map route visualization and search history. Unregistered users receive five free searches per day. Logging into an account restores saved search history for container tracking and ship schedules, alongside air cargo queries.

### Intermodal Route Planner API
The release of the Route Planner API gives logistics teams programmatic control over custom route builds within their intermodal route planning software. Users can define custom legs across seaports, airports, plus road and rail terminals. Each node supports specific transport modes and event milestones.

Every custom route generates a unique ID number. This ID simplifies sharing with customers and enables quick lookup in the Tracking System. The API can also complete routing structures automatically and populate missing location details upon request.

### Demurrage & Storage Calculator
Fee estimation tools received a dedicated backend. The Demurrage & Storage Calculator API is now live, accompanied by expanded documentation in the Developer Portal.

The web calculator updated its interface to support demurrage and storage risk calculation. Users can check valid date ranges, select import or export modes, calculate costs in preferred currencies, and download summary reports as PDF files.

### Virtual Office and Infrastructure
Workflow updates affected two Virtual Office modules:
* **Bookings Tab:** Updated logic supports additional data fields within transport details across every shipping mode.
* **Counterparties Panel:** Link generation logic was updated. Invite links now issue under SeaRates.com or under a client's custom platform domain.

Developer infrastructure received two final enhancements. SeaRates released a web-integrated Request a Quote component, adding ready-to-use snippets to the logistics API integration workflow. In addition, the Geocoding API database expanded to 18,000 global seaports, fully synchronized with data from the World Sea Ports app.
"""

# Check Layer 3 rhetorical patterns
print("=== LAYER 3 ANALYSIS ===")

# Contrastive negation check
negations = re.findall(r'\b(not|rather than|instead of|no|never)\b', draft_text, re.I)
print(f"Contrastive Negation matches: {negations}")

# Over-explaining connectors / transitions
transitions = ["moreover", "furthermore", "additionally", "in addition", "finally", "that's why", "as a result", "consequently", "in order to"]
found_transitions = []
for t in transitions:
    matches = re.findall(r'\b' + re.escape(t) + r'\b', draft_text, re.I)
    if matches:
        found_transitions.append((t, len(matches)))
print(f"Transitions found: {found_transitions}")

# Participial / balancing phrase structure check
participials = re.findall(r'\b\w+ing\b', draft_text)
print(f"Participial '-ing' count: {len(participials)} (e.g., {participials[:10]})")

# Sentence length variance
sentences = re.split(r'[.!?]+', draft_text)
sentences = [s.strip() for s in sentences if len(s.strip()) > 5]
sentence_lengths = [len(s.split()) for s in sentences]
print(f"Sentence count: {len(sentences)}")
print(f"Sentence length distribution (words): {sentence_lengths}")
print(f"Average sentence length: {sum(sentence_lengths)/len(sentence_lengths):.1f} words")

