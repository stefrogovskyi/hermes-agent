import re

draft_text = """Title: SeaRates Mobile App: Request Quotes for Freight & Warehouses
Meta-Title: SeaRates App Request System: Fast Freight & Storage Quotes
Meta-Description: Submit a mobile quote request for cargo shipping or a warehousing rate inquiry in the SeaRates app, with custom offers from verified logistics providers.

Body:
SeaRates has added a Request System to its iOS and Android mobile app, giving shippers a single point to submit freight and storage requirements. Available under the Tools menu after signing up, the feature requires no special account permissions. The interface splits directly into two main tabs, handling cargo shipping quotes on one side and a warehousing rate inquiry on the other.

Submitting a Freight Quote

The cargo section begins with a category drop-down list covering 23 commodity types. Shippers can flag items with additional parameters: Hazardous, Perishable, Oversize, or Liquid. Selecting Hazardous opens prompt fields for the UN number and a full list of IMO Classes. Choosing Perishable brings up Humidity and Temperature entries. Oversize requests require Width, Height, and Length dimensions, while Liquid cargo needs no extra parameter fields before proceeding.

Moving to the request details section, selecting the transport mode adjusts the remaining form fields. Options include:
Sea shipping: automatic default for all transportation, FCL, LCL, and Bulk
Road transport: FCL, FTL, and LCL
Rail transport: FWL
Air freight: Standard cargo or ULD Container

Users then enter departure and arrival points, the cargo readiness date, and select Freight To Pay Basis terms from the list.

Before submitting a mobile quote request, shippers can attach supplementary services to the calculation without generating separate inquiries. These include insurance, customs clearance, certification, inspection services. Shippers needing financing can also apply directly for the SeaRates Logistics & Trade Finance program, which covers Invoice Factoring, Invoice Discounting, Reverse Factoring, Trade Payables Financing, and Inventory Financing. An open text field for additional information allows shippers to specify preferences regarding cost, preferred carriers, or shipment urgency.

Submitting a Warehousing Rate Inquiry

Building a warehousing rate inquiry follows a similar path. The user selects the commodity category and applies any relevant extra parameters for hazardous, perishable, oversized, or liquid goods under cargo details.

The request details section then prompts for specific warehouse parameters:
Storage type: open, covered, fulfillment center, or refrigerated
Facility status: bonded or non-bonded
Location and ZIP code
Space requirement and booking timeframe
Search radius filter within the chosen country

In addition, users can bundle specific warehouse operations into their quote request: insurance, customs clearance, certification, inspection services, handling, stuffing, survey, fulfillment, storage, packing, marking, palletization, and railway services. After reviewing the entries and adding any final comments, pressing Send submits the form.

Verification and Supplier Responses

Completing either form takes seconds. Once submitted, each request and participating supplier undergoes multi-stage verification by the SeaRates team. Responses come from vetted carriers, freight forwarders, warehouse operators, and 3PLs whose safety, operational quality, and reliability have been confirmed. Shippers receive detailed, transparent freight and storage offers aligned with their exact parameters.

White-Label App Integration for Logistics Businesses

Logistics providers and transport companies can adopt this system through a white-label logistics app integration. By applying their own logo and company branding to the SeaRates app architecture, freight businesses can offer their customers a branded portal for digital freight quoting and storage inquiries. Shippers log in directly under the provider's brand to request customized rates, while the provider maintains a structured channel for instant freight quotation workflows."""

# Check for AI transition words and phrases
transitions = [
    "in addition", "additionally", "furthermore", "moreover", "however", "therefore", "thus", 
    "consequently", "as a result", "moving to", "building a", "completing either", "before submitting",
    "by doing so", "helps ensure", "designed to", "aims to", "serves as", "it is important to note",
    "in order to", "so as to", "as well as"
]

for t in transitions:
    matches = re.findall(rf'\b{re.escape(t)}\b', draft_text, re.IGNORECASE)
    if matches:
        print(f"Transition/Filler phrase '{t}': {len(matches)}")

# Check for grammatical minor issue in paragraph 5:
# "These include insurance, customs clearance, certification, inspection services."
print("\nGrammar check on paragraph 5 sentence:")
for line in draft_text.split('\n'):
    if "These include" in line:
        print("Line:", line)

