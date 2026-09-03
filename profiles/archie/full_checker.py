import json

title = "Blank Sailings 2025: Tariff War and Capacity"
meta_title = "Blank Sailings 2025 and Ocean Freight Tariffs"
meta_description = "Carriers cut capacity as ocean freight tariffs rise. Track blank sailings 2025 and vessel schedule reliability with SeaRates supply chain visibility API."

body = """Ocean carriers manage market turbulence by erasing scheduled voyages from global trade maps. When a shipping line implements a blank sailing, it cancels a planned voyage or skips specific port calls along a route. The service is entirely removed rather than delayed, creating immediate reductions in available shipping space, unpredictable transit times, and disruption across global supply chain schedules.

Proposed U.S. import duties, new ocean freight tariffs, and Donald Trump's 2025 tariff plans have raised renewed fears of a trade war between the US and China. Shippers are accelerating moves to front-loading shipments from Asia to beat impending cost increases. Retailers and manufacturers build inventory buffers before rate hikes take effect, causing brief spikes in booking volumes followed by steep drops in demand. This volatility undermines schedule stability and leaves carriers with excess vessel capacity. To protect spot rates from collapsing, global carriers resort to carrier alliances blanking strategy across major trade corridors, particularly trans-Pacific and Asia-Europe routes.

The resulting transpacific container capacity reductions show up clearly in market data:

- Asia to North America West Coast capacity fell 12% over six weeks, dropping from 1.43 million to 1.37 million TEU.
- Asia to North America East Coast capacity declined 14%, moving from 1.01 million to 867 thousand TEU.
- Peak weeks see 28% to 42% of total weekly capacity withdrawn through cancelled sailings.
- Major U.S. gateways like Los Angeles and Long Beach report average vessel delays of 7-10 days, overloading regional warehouse networks.
- As of April 17, 2025, the Drewry World Container Index stood at $2,192 per 40-foot container, down 3% from the prior week.

Port congestion and delays at Chinese hubs have forced widespread service adjustments. Carriers have suspended direct sailings between major Chinese ports and U.S. destinations or rerouted cargo through Mediterranean hubs. Feeder networks face heavy strain, transshipment delays are rising, and smaller European ports struggle to absorb uneven cargo arrivals.

Contract dynamics are shifting alongside physical routes. Smaller shippers and SMEs lacking volume leverage face cargo bumps despite signed contracts. Conversely, large BCOs renegotiate long-term agreements by accepting higher base rates to lock in priority space guarantees. Major groups including Ocean Alliance and THE Alliance have consolidated operations into fewer port calls. Although vessel schedule reliability remains above 85%, actual weekly sailing frequency continues to fall as alliances choose to blank voyages rather than operate underbooked ships.

Logistics teams are responding with multi-layered tactics:
- Nearshoring manufacturing operations to Southeast Europe or Mexico.
- Rerouting cargo through regional ports such as Gdańsk, Valencia, and Savannah.
- Shifting time-sensitive shipments to air freight.
- Deploying digital logistics platforms to monitor capacity changes.

Market conditions in Q3 and Q4 of 2025 threaten to deepen this split landscape. Without a stable peak season, rate volatility, space restrictions, and sudden port skips will persist.

Practical actions for retail businesses:
- Build buffer time for international shipment delays.
- Monitor cost fluctuations across imported inventory lines like clothing, electronics, and groceries.
- Compare freight rates across multiple carriers and suppliers.
- Align purchasing timelines to mitigate stockout risks.

Practical actions for enterprise operations:
- Audit supply chain dependencies and identify vulnerable bottlenecks.
- Diversify vendor networks and transport routes.
- Implement real-time shipment tracking across all trade lanes.
- Apply predictive analytics to model disruption risks and support data-driven decisions.
- Work with logistics specialists to develop tailored contingency plans.
- Hold safety stock to buffer against extended transit delays.

Managing blank sailings 2025 requires real-time cargo visibility. SeaRates provides container tracking tools to monitor route changes, customs events, and schedule updates. The platform tracks shipments by container, bill of lading, or booking number using data from more than 200 shipping lines and leasing companies worldwide. Operators can monitor transit times, predictive ETAs, and up to 25 shipment exceptions to anticipate delays. Integrating these tools via web tools or the SeaRates supply chain visibility API provides the data needed to maintain control across volatile ocean routes."""

data = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_description,
    "body": body
}

full_text = f"{title}\n{meta_title}\n{meta_description}\n{body}"

# Check rule 1: Em-dash and double hyphen
assert "—" not in full_text, "Error: Em-dash found"
assert "--" not in full_text, "Error: Double hyphen found"

# Check rule 9: Lengths
assert len(title) <= 60, f"Title length {len(title)} > 60"
assert len(meta_title) <= 60, f"Meta title length {len(meta_title)} > 60"
assert len(meta_description) <= 155, f"Meta desc length {len(meta_description)} > 155"

# Check rule 5: Connectors
for conn in ["that's why", "which is why", "this explains why"]:
    assert conn not in full_text.lower(), f"Forbidden connector: {conn}"

# Check keywords
keywords = [
    "blank sailings 2025",
    "ocean freight tariffs",
    "front-loading shipments",
    "transpacific container capacity",
    "vessel schedule reliability",
    "Drewry World Container Index",
    "port congestion and delays",
    "carrier alliances blanking",
    "supply chain visibility API"
]
for kw in keywords:
    assert kw.lower() in full_text.lower(), f"Missing keyword: {kw}"

# Check mandatory facts
required_facts = [
    "12%", "1.43 million", "1.37 million", "14%", "1.01 million", "867 thousand",
    "28%", "42%", "7-10", "$2,192", "April 17, 2025", "3%", "85%", "200", "25",
    "Ocean Alliance", "THE Alliance", "SeaRates",
    "Los Angeles", "Long Beach", "Gdańsk", "Valencia", "Savannah",
    "Southeast Europe", "Mexico", "clothing", "electronics", "groceries",
    "Donald Trump", "Q3", "Q4"
]
for rf in required_facts:
    assert rf.lower() in full_text.lower(), f"Missing required fact: {rf}"

print("JSON OUTPUT:")
print(json.dumps(data, indent=2))

