import re

title = "Using SeaRates Logistics Map for Cargo Quotes and Tenders"
meta_title = "SeaRates Logistics Map: Quote & Request Cargo Shipping"
meta_desc = "Learn how to post requests, get quotes, and manage available freight capacity using the SeaRates interactive freight map for shippers and carriers."

body = """Cargo owners with tight shipment schedules and carriers searching for profitable loads often end up searching in opposite directions. The SeaRates Logistics Map pulls both sides into a single operational view. Shippers run a real-time RFQ and cargo tender platform to gather quotes, while transport providers find direct leads to fill available market capacity.

Open the Logistics Map in your SeaRates account and switch to the Cargoes tab. The interface adjusts depending on whether you are submitting cargo details or reviewing existing market entries.

### How shippers post requests and review rates

When you need to ship a one-off load or manage regular cargo traffic, posting an entry starts with the Request a Quote button. Fill out the form with container counts, weight, cargo types, origin and destination points, and target loading dates. Add specific requirements if your load needs temperature control or special handling instructions, then send it off.

Once submitted, the inquiry sits directly on the map. Detailed parameters yield better targeted quotes from carriers. You can also monitor live market activity directly through the interactive freight map:

* Enter origin and destination locations to view current inquiries.
* Review request cards showing container types, ready-to-load dates, and requested add-on services.
* Open individual cards to check geographic routes, copy shareable links, or click View all available offers in the upper right corner to open Logistics Explorer and inspect active market tariffs.
* Filter listings by loading readiness, transport mode, warehouse requirements, commodity type, or location.
* Toggle settings to view expired requests or items you submitted previously, or zoom into specific geographic zones.

Quotations land straight in your Virtual Office. You compare offers by pricing, timelines, and service terms before booking directly. The tool covers sea, air, rail, and road freight routes.

### Quoting loads for carriers, forwarders, and 3LPs

Logistics providers and forwarders use the same Cargoes tab to source business without cold calling. Filtering by location or loading date brings up active shipper requests complete with cargo weights, service notes, and route points.

If you need to fill a single container or build up an FCL shipment out of multiple LCL inquiries, zoom into target regions. Forwarders balancing container movement across specific corridors like Canada or South Africa can scan regional cards for exact fits.

Clicking Quote on any request card transfers that lead directly into your Virtual Office for further negotiation. An embedded chat connects you with SeaRates Support if questions arise during quotation. Idle capacity turns into active revenue pipelines without manual outreach.

### Site integration and API features

Companies can embed this white-labeled tool directly into their own websites. Shippers get a custom tender portal, while carriers run a branded map to collect client leads. Documentation and integration demos are available on request.

For deeper system integration, the Logistics Map API syncs data directly into custom software or enterprise platforms like SAP. It automates freight requests and quote matching across existing workflows:

* Direct uploading of cargo requests and transport services
* Feed real-time leads and filtered requests into your ERP or TMS
* Manage dynamic pricing models and formal tender submissions

For API access or tailored setup, contact it.sales@searates.com. Additional features covering the Transport and Warehouses tabs will follow in upcoming updates."""

print(f"Title ({len(title)}): {title}")
assert len(title) <= 60

print(f"Meta Title ({len(meta_title)}): {meta_title}")
assert len(meta_title) <= 60

print(f"Meta Desc ({len(meta_desc)}): {meta_desc}")
assert len(meta_desc) <= 155

# Check em-dashes
assert "—" not in title and "—" not in meta_title and "—" not in meta_desc and "—" not in body
print("Em-dash check passed.")

# Check email
assert "it.sales@searates.com" in body
print("Email check passed.")

# Check terms
assert "return loads" not in body
assert "profitable loads" in body
assert "idle vehicle or vessel space" not in body
assert "idle capacity" in body
print("Grounded terms check passed.")

