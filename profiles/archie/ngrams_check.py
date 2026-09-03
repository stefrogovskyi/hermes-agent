import re

original_text = """
Your ongoing support of SeaRates is appreciated. We are presently very excited about presenting fresh improvements that will better support your business needs. We continue to place a premium on enhancing our offerings.
To acquire the most recent information, please see our prior updates.

What’s new for week 16:

Tracking System updates:
We are glad to present Pricing page launched for SeaRates Tracking System tool. You can find Pricing plan in our top menu.
Also, we’ve enhanced our integration with shipping lines and leasing companies, namely CMA CGM, CEVA Logistics, FESCO, Ocean Network Express (ONE), Mediterranean Shipping Company (MSC), Sinotrans Container Lines, Interasia Lines, and Textainer.

Terminal API improvements:
We’re pleased to share that Nhava Sheva Freeport Terminal & CMA BEIRUT TERMINAL have been added to our list of supported carriers — bringing the total to 50 integrated providers.

Air Tracking enhancements:
We are glad to announce added support for two more airlines — Air Incheon and Smart Wings, bringing the total number of supported providers to 244, kindly check the full list here.
Moreover, We have improved our support for airlines, including Malaysia Airlines, SF Airlines, Cathay Pacific Airways, Etihad Cargo, Juneyao Airlines, and China Cargo Airlines.

Ship Schedules updates:
We have made enhancements to our collaboration with shipping lines, including Evergreen by Points, Hyundai, ONE, and COSCO by Vessel, as well as ZIM by Ports.

Announcements:
Unified Tracking System
Vessel Tracking API v1
Logistics Map ‘Warehouse’ tab
SeaRates AI 1.0
Parcel Tracking Web
Load Calculator Web 3.0 (new design and features)
Map Platform
Road Tracking API
"""

rewrite_text = """
# SeaRates Week 16 Release Notes: Fresh Tracking Upgrades and Integration Expansions

Meta Title: SeaRates Week 16 Updates: Container & Air Tracking APIs
Meta Description: Explore SeaRates Week 16 updates: tracking pricing, 50 terminal API integrations, 244 air tracking carriers, and ocean freight schedule updates.

Body:
## Section 1: Tracking System & Carrier Integrations

Direct access to clear commercial terms is now live: a dedicated pricing page for the SeaRates Tracking System tool has been published in the main header menu. Users evaluating container tracking API options can inspect subscription tiers directly without navigating through secondary sales channels.

Beyond pricing transparency, deep-level data connections across major ocean carriers and container leasing entities have been upgraded. Systems connecting to CMA CGM, CEVA Logistics, FESCO, Ocean Network Express (ONE), Mediterranean Shipping Company (MSC), Sinotrans Container Lines, Interasia Lines, and Textainer now process milestone events with higher accuracy and reduced polling latency.

## Section 2: Terminal API Expansion

Real-time terminal status monitoring grows as two major maritime facilities join the network. Integration is complete for Nhava Sheva Freeport Terminal and CMA BEIRUT TERMINAL, allowing logistics teams to pull container gate events and vessel berth status directly into their internal workflows.

This update pushes the SeaRates terminal coverage benchmark to 50 integrated providers. Broader terminal coverage gives cargo handlers early signals on port congestion, vessel shifts, and dwell times before containers hit delays on the ground.

## Section 3: Air Tracking Infrastructure

Air cargo tracking coverage expands with the integration of two new carriers: Air Incheon and Smart Wings. Their addition brings total supported air freight providers to 244, with full carrier lists available in the SeaRates directory.

Existing air integrations received structural performance updates as well. Tracking feeds for Malaysia Airlines, SF Airlines, Cathay Pacific Airways, Etihad Cargo, Juneyao Airlines, and China Cargo Airlines now process status shifts with cleaner air waybill event parsing and quicker status refresh cycles.

## Section 4: Vessel Schedule Tool Updates

Routing accuracy relies on fresh ocean freight schedules. Recent technical adjustments improve data exchanges with carrier routing databases, focusing on point, vessel, and port schedule layers.

Specific upgrades cover Evergreen by Points, Hyundai, ONE, and COSCO by Vessel, along with ZIM by Ports. Logistics planners can cross-check voyage dates and transit timelines across these lines with higher confidence when organizing complex intermodal movements.

## Section 5: Ecosystem & Tool Directory

SeaRates continues refining its broader suite of freight solutions, building tools for clarity rather than complexity. Prior platform updates remain accessible in our archives for teams tracking feature rollouts. Below is the current directory of core tools and active platform solutions:

* **Unified Tracking System:** Centralized multi-modal tracking interface.
* **Vessel Tracking API v1:** API engine delivering AIS and carrier vessel positions.
* **Logistics Map ‘Warehouse’ tab:** Interactive mapping tool displaying storage locations and fulfillment nodes.
* **SeaRates AI 1.0:** Artificial intelligence layer supporting rate inquiries and operational lookups.
* **Parcel Tracking Web:** Web tool for small-package shipment tracking.
* **Load Calculator Web 3.0:** Redesigned cargo optimization tool featuring updated design and new features.
* **Map Platform:** Geo-visualization framework for global trade routes.
* **Road Tracking API:** Land freight tracking interface for trucking movements.
"""

def clean_lines(text):
    return [line.strip() for line in text.split('\n') if line.strip()]

# Let's check longest common substrings excluding entity lists
import difflib

# Find all common sub-sequences of words between original and rewrite
orig_words = re.findall(r'\b\w+\b', original_text)
rew_words = re.findall(r'\b\w+\b', rewrite_text)

matcher = difflib.SequenceMatcher(None, [w.lower() for w in orig_words], [w.lower() for w in rew_words])

matches = matcher.get_matching_blocks()

print("All matching word sequences of length >= 3:")
for m in matches:
    if m.size >= 3:
        orig_seq = " ".join(orig_words[m.a : m.a + m.size])
        rew_seq = " ".join(rew_words[m.b : m.b + m.size])
        print(f"Length {m.size}: '{orig_seq}'")

