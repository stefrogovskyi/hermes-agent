import json, re

# Let's write the draft python script to test character lengths, em-dashes, and required changes.

title = "SeaRates Records First AI Agent Booking Without Clicks"
meta_title = "First AI Agent Freight Booking Completed on SeaRates"
meta_desc = "On July 22, 2025, a shipper booked cargo from Shanghai to Hamburg via an OpenAI MCP agent on SeaRates without moving a mouse."

body_text = """On July 22, 2025, cargo was booked on the Shanghai to Hamburg route without a human hand touching a computer mouse.

The shipper secured the lowest available rate on SeaRates using artificial intelligence. This happened right after OpenAI launched its AI Agent mode on July 21. That new capability synchronized with SeaRates digital tools through Model Context Protocol (MCP) technology. Instead of clicking through menus, the user handed the operational work to a virtual agent.

The software handled rate comparison, document processing, and final booking in real time.

How the Booking Happened

The entire setup took minutes:

1. Log into SeaRates and open ChatGPT.com.
2. Enter the route from Shanghai to Hamburg and select a 40-foot container. Add specific cargo parameters like item type, total weight, and optional logistics services.
3. Ask the agent to audit all available rates and pick the cheapest option.
4. The AI agent navigates to Logistics Explorer, populates all required shipment details, and prompts you for permission to finalize the booking.
5. Watch the cursor move and read live updates in the chat window. You retain full control to confirm, adjust, or cancel the transaction at any moment.
6. Once approved, the system generates the booking and saves it directly to your SeaRates Virtual Office under the Activity tab within Bookings and Requests.

What Happens After Placing the Order

AI handles the initial booking, but physical cargo still follows standard shipping procedures. Following the booking, the AI assistant generates an example step-by-step operational checklist to guide the shipper through execution, outlining reference details such as a $3,456 invoice and a sample payload of 22 tons of aluminum.

First, SeaRates emails a booking confirmation containing payment instructions. Once payment clears and space is allocated on the vessel, cargo preparation begins. The shipper assembles export documentation, including the commercial invoice, packing list, and relevant certificates. The carrier then assigns an empty 40-foot container in Shanghai, which the shipper retrieves, loads, and seals.

Export customs clearance in China must be completed prior to loading, with SeaRates offering direct assistance if needed. Once loaded, the container boards the vessel, and shippers can monitor live location updates using the Track Booking Status tool on SeaRates.

When the ship arrives at Hamburg, import customs clearance begins. Prepare all necessary documents and clarify requirements in advance. Finally, following customs release, the shipper coordinates with the port terminal to schedule container pickup and arrange inland transit to the final destination.

AI Agents in Freight Management

Detailed research by Alexei Shatunov on LinkedIn highlights machine learning and AI applications across global supply chains. These MCP agents give shippers a direct way to handle freight bookings, track shipments, and eliminate repetitive administrative steps.

For inquiries about configuring AI freight management agents, reach out to sales@searates.com."""

# Check lengths
print(f"Title len: {len(title)} (max 60)")
print(f"Meta-Title len: {len(meta_title)} (max 60)")
print(f"Meta-Desc len: {len(meta_desc)} (max 155)")

# Check em dashes
full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body_text}"
has_em_dash = '—' in full_text or '--' in full_text or '–' in full_text
print(f"Has em dash / en dash / double hyphen: {has_em_dash}")

# Check filler phrases removed
print("'Here is how it worked.' in meta_desc:", "Here is how it worked." in meta_desc)
print("'Here is the exact process the shipper used:' in body:", "Here is the exact process the shipper used:" in body_text)
print("'Research and Future Directions' in body:", "Research and Future Directions" in body_text)

# Check intro phrasing
print("'moved from Shanghai to Hamburg' in body:", "moved from Shanghai to Hamburg" in body_text)

# Check fact-check clarification
print("Fact check mentioned example/sample:", "example step-by-step operational checklist" in body_text)

# Check prevents port delays removed
print("'prevents port delays' in body:", "prevents port delays" in body_text)
print("'Prepare all necessary documents and clarify requirements in advance' in body:", "Prepare all necessary documents and clarify requirements in advance" in body_text)

