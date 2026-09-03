# Factual Verification Matrix Script

claims = [
    {
        "rewrite_claim": "20-foot container: USD $2,000 to $4,000",
        "source_match": "- 20-foot container: USD $2,000–$4,000",
        "status": "VERIFIED"
    },
    {
        "rewrite_claim": "40-foot container: USD $3,500 and $6,500",
        "source_match": "- 40-foot container: USD $3,500–$6,500",
        "status": "VERIFIED"
    },
    {
        "rewrite_claim": "Quotes cover ocean freight, though packing services, transit insurance, local port fees, and last-mile delivery within Singapore often incur extra charges",
        "source_match": "These prices include ocean freight but may exclude additional charges such as packing, insurance, local port fees, or last-mile delivery in Singapore.",
        "status": "VERIFIED"
    },
    {
        "rewrite_claim": "Shipments originating from distant regions like Europe or North America carry higher baseline prices than regional runs from Malaysia or Indonesia",
        "source_match": "shipping from the U.S. or Europe is more expensive than from Malaysia or Indonesia",
        "status": "VERIFIED (U.S. -> North America)"
    },
    {
        "rewrite_claim": "High-density ocean routes out of major transport hubs such as London, New York, or Sydney remain cheaper and faster than obscure secondary lanes",
        "source_match": "Popular routes from major cities like London, New York, or Sydney are generally more affordable and faster than lesser-used routes.",
        "status": "VERIFIED"
    },
    {
        "rewrite_claim": "FCL charges a single flat rate for the entire container regardless of occupied space, fitting full-house relocations",
        "source_match": "FCL (Full Container Load): Best for full-house moves. You pay a flat rate for the whole container, regardless of how much space you use.",
        "status": "VERIFIED"
    },
    {
        "rewrite_claim": "LCL fits smaller moves by grouping multiple shipments inside shared space where you pay strictly for the volume used",
        "source_match": "LCL (Less-than Container Load): Ideal for smaller moves. You share a container and pay only for the volume you use.",
        "status": "VERIFIED"
    },
    {
        "rewrite_claim": "Peak shipping surges hit between June and August, then return from December through January",
        "source_match": "Moving in peak months (June–August and December–January) can result in higher rates due to demand surges.",
        "status": "VERIFIED"
    },
    {
        "rewrite_claim": "Booking moves months ahead of these windows reduces baseline costs",
        "source_match": "Booking early can save you both time and money.",
        "status": "VERIFIED"
    },
    {
        "rewrite_claim": "Sea freight household goods Singapore shipments require 3 to 6 weeks",
        "source_match": "Sea Freight: Delivery Time: 3–6 weeks",
        "status": "VERIFIED"
    },
    {
        "rewrite_claim": "Air freight cuts transit time to 5 to 10 days, but expenses jump to 3 to 5 times the price of ocean transport",
        "source_match": "Air Freight: Delivery Time: 5–10 days; Cost: 3–5x more expensive than sea freight",
        "status": "VERIFIED"
    },
    {
        "rewrite_claim": "Many households use a hybrid plan: air cargo carries immediate essentials, while sea vessels handle furniture, kitchenware, books, and bulk items",
        "source_match": "Some families choose a hybrid solution — sending essentials by air and the rest by sea... Sea Freight Best for: Furniture, kitchenware, books, and personal belongings... Air Freight Best for: Urgent items...",
        "status": "VERIFIED"
    },
    {
        "rewrite_claim": "Singapore customs duty-free household import regulations apply to personal belongings that are already used and declared properly upon arrival",
        "source_match": "household effects are duty-free if used and declared correctly",
        "status": "VERIFIED"
    },
    {
        "rewrite_claim": "Restricted goods like alcohol, prescription medications, and consumer electronics may require permits or import tariffs",
        "source_match": "restricted items (e.g., alcohol, medication, or electronics) may be levied a charge or require permits.",
        "status": "VERIFIED"
    },
    {
        "rewrite_claim": "Chewing gum, controlled drugs, and specific dietary supplements face strict import bans or heavy regulations",
        "source_match": "Certain goods (e.g., chewing gum, controlled drugs, some supplements) are strictly regulated or banned.",
        "status": "VERIFIED"
    },
    {
        "rewrite_claim": "International movers operating in Southeast Asia should provide transparent door-to-door quotes specifying whether customs clearance and unpacking are included",
        "source_match": "Look for companies experienced with Southeast Asia and transparent pricing... Does it include door-to-door service, customs clearance, and unpacking?",
        "status": "VERIFIED"
    },
    {
        "rewrite_claim": "Obtaining quotes from 2 to 3 international movers helps benchmark true market rates",
        "source_match": "Compare quotes from 2–3 reputable international movers.",
        "status": "VERIFIED"
    },
    {
        "rewrite_claim": "Detailed, numbered box inventories accelerate clearance at port checkpoints and substantiate transit insurance claims for fragile goods",
        "source_match": "Prepare a detailed inventory. It will speed up customs clearance and help with insurance claims if needed. Label and number all boxes clearly... insurance... especially for fragile or high-value items.",
        "status": "VERIFIED"
    },
    {
        "rewrite_claim": "Financing an overseas move using an unsecured loan can be evaluated through comparison platforms like ROSHI to compare interest rates and loan terms",
        "source_match": "If you're considering using an unsecured loan to finance your move to Singapore, explore platforms such as ROSHI to secure the lowest rates and competitive terms.",
        "status": "VERIFIED"
    }
]

print("=== LAYER D: FACTUAL VERIFICATION MATRIX ===")
for i, c in enumerate(claims, 1):
    print(f"{i}. REWRITE: {c['rewrite_claim']}")
    print(f"   SOURCE : {c['source_match']}")
    print(f"   STATUS : {c['status']}\n")
