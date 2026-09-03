import re

source = """We appreciate your continuing support for SeaRates. We are glad to introduce new solutions and upgrades that will better satisfy your trading and logistics requirements. Our team continues to prioritize the improvement of our services.
To acquire the most recent information, please see our prior updates.

What’s new for week 15:
Tracking System updates:
We’re pleased to share that Euroconsol & Hugo Stinnes have been added to our list of supported carriers — bringing the total to 198 integrated providers. You can view the entire updated list in our API documentation here.
Moreover, we have made enhancements to our collaboration with shipping lines, including the following:
Gold Star Line, DSV Ocean Transport, ZIM, CEVA Logistics, Orient Overseas Container Line (OOCL), and Yang Ming.

Road Tracking improvements:
We have improved our support for providers, including TForce Freight.

Terminal API enhancements:
Our team is glad to announce added support for two more terminals, namely CSP Abu Dhabi and CSP Zeebrugge.

Air Cargo Tracking updates:
We’ve enhanced our integration with airlines, namely Cathay Pacific Airways, Juneyao Airlines, China Cargo Airlines, and Malaysia Airlines.

Logistics Explorer improvements:
Sign up for SeaRates.com to access instant chat with our Support Team right next to the rate result card.

Ship Schedules enhancements:
We have made enhancements to our collaboration with shipping lines, including ONE and Shipping Corporation of India by Points, Yang Ming by Ports, as well as for Namsung, ZIM, CMA CGM, APL, ANL, and CNC by Vessel.

Announcements / Platform capabilities:
Unified Tracking System, Vessel Tracking API v1, Logistics Map 'Warehouse' tab, SeaRates AI 1.0, Parcel Tracking Web, Load Calculator Web 3.0, Map Platform, Road Tracking API."""

title = "SeaRates Release Notes: Week 15, 2025"
meta_title = "SeaRates Product Updates | Week 15, 2025"
meta_desc = "SeaRates added Euroconsol and Hugo Stinnes to its tracking network, updated Terminal API, air cargo tracking, and added instant chat to Logistics Explorer."

body = """Logistics data stays useful only when the connections behind it remain fresh.

Our tracking network now includes Euroconsol and Hugo Stinnes. That addition brings our integrated carrier roster up to 198 providers. The complete list remains available inside our API documentation.

We also updated tracking integrations for several ocean shipping lines, including DSV Ocean Transport, Gold Star Line, and ZIM, as well as CEVA Logistics, Yang Ming, and Orient Overseas Container Line (OOCL). For ground freight, road tracking support was updated for TForce Freight among other providers.

The Terminal API expanded its coverage with two new facilities: CSP Abu Dhabi and CSP Zeebrugge.

Air cargo tracking saw updates across four carriers: Cathay Pacific Airways, China Cargo Airlines, Juneyao Airlines, and Malaysia Airlines.

For rate searches on SeaRates.com, registered users now have access to live support directly alongside the rate result card.

Ship Schedules received structural updates across multiple search modes. Point-based searches were updated for ONE and Shipping Corporation of India. Port-based searches received enhancements for Yang Ming. Vessel-level search tracking was updated for ZIM, Namsung, CMA CGM, APL, CNC, and ANL.

Alongside these updates, SeaRates continues supporting operations across its broader platform suite. Key components include SeaRates AI 1.0, the Vessel Tracking API v1, and the Unified Tracking System. Additional capabilities span the Warehouse tab on Logistics Map, Load Calculator Web 3.0, Parcel Tracking Web, Road Tracking API, and the main Map Platform."""

full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

print("=== CHECKING LENGTHS ===")
print(f"Title ({len(title)} <= 60): {len(title) <= 60}")
print(f"Meta Title ({len(meta_title)} <= 60): {len(meta_title) <= 60}")
print(f"Meta Desc ({len(meta_desc)} <= 155): {len(meta_desc) <= 155}")

print("\n=== LAYER A: 6-GRAM OVERLAP AUDIT ===")
def get_ngrams(text, n=6):
    words = [w.lower() for w in re.findall(r'\b\w+\b', text)]
    return set(zip(*[words[i:] for i in range(n)]))

source_6grams = get_ngrams(source)
body_6grams = get_ngrams(body)
overlap_6grams = source_6grams.intersection(body_6grams)
print("6-gram overlaps count:", len(overlap_6grams))
print("6-gram overlaps:", [" ".join(g) for g in overlap_6grams])
