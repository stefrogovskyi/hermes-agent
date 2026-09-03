import re

rewr = """
Five years of continuous supply chain disruption may give way to smoother global trade in 2026, yet two quiet triggers could rewrite shipping budgets overnight. A sudden reopening of the Red Sea and Suez Canal alongside sudden inventory stockpiling in the United States stand out as primary forces behind potential market shifts.

Baseline market projections point to an average ocean freight rate drop of 30% to 35% in 2026 compared to 2025 levels. For a standard 40-foot high cube (40'HC) container moving from Asia to the US West Coast, baseline figures point toward $2,200 to $3,200. Market data from November 2025 indicates that unexpected supply shocks could rapidly drive those same rates above $9,500 within weeks.

The global container ship fleet will add 1.4 million TEU in capacity during 2026, representing a 5% increase in total ocean capacity. While headlines warn of container fleet capacity oversupply, 70% to 80% of these new vessels will enter secondary routes across Africa, Latin America, and India instead of main trade lanes. Demand across those secondary markets expands by 10% to 15% annually.

Tonnage shortages on primary trade lanes between Asia and Europe or North America will persist, preventing rate collapses. Main trade routes face frequent General Rate Increase (GRI) and Peak Season Surcharges (PSS) spikes, keeping spot rate volatility between $2,000 and $3,000.

Simultaneously, more than 13% of the global fleet (exceeding 4 million TEU) is over 20 years old and due for scrapping. Scrapping old vessels offsets the new production capacity, keeping net fleet growth around 2% to 3%.

Rates on Asia to Northern Europe trade routes should remain around $3,500 to $4,500 during this mild downturn, staying well clear of an $1,800 floor. Major ocean carriers manage capacity actively. Maersk and Hapag-Lloyd within the Gemini Alliance restructured 57 services into a hub-and-spoke model, cutting direct voyages to stretch tonnage across network nodes. Gemini Alliance hub-and-spoke reliability allows carriers to maintain high schedule discipline. Meanwhile, MSC and CMA CGM use blank sailings (canceling 5% to 10% of sailings in November and December 2025) while parking 1% to 2% of their total fleet in lay-up.

Nearly 95% of global ocean vessels have avoided the Suez Canal since December 2024 due to regional geopolitical conflicts, rerouting around the Cape of Good Hope in South Africa. The ongoing choice between Suez Canal routing vs Cape of Good Hope navigation remains a central variable for global supply chains.

Analyst estimates assign a 40% to 50% probability that the canal reopens during the first half of 2026. A ten-month truce, a halt in Houthi maritime attacks, and reduced insurance premiums (now down to 0.3%–0.7%) have prompted carriers like ZIM and CMA CGM to test return passages. Carriers stand ready to resume full Red Sea routing once attack frequencies drop below one or two per month.

A sudden canal reopening would return 15% to 20% of effective global fleet tonnage to the market almost overnight. The operational aftermath would be severe:

* European ports would experience 4 to 8 weeks of severe congestion as weekly ship arrivals double.
* Congestion surcharges ranging between $1,500 and $3,000 per container would take effect immediately.
* Asia would face a 40'HC equipment shortage lasting 2 to 3 months.
* Inland road and rail networks would bottleneck as land transport adapts to altered intermodal container flows.

American importers remain cautious, restricting order sizes to immediate inventory needs due to tariffs on goods originating from China. Sourcing has shifted heavily toward India, Mexico, and Vietnam, whose combined trade volume now exceeds total European Union shipments to the US.

Any reduction in tariff barriers, economic acceleration, or post-election clarity will prompt importers to rebuild inventories rapidly. A sudden surge in US import tariff frontloading could increase ocean cargo volumes by 30% to 40% within the first 2 to 3 months.

If rapid US inventory restocking coincides with a Red Sea reopening, surging import demand meets an abrupt surplus of vessel capacity and equipment. Within 4 to 6 weeks, rates for a 40-foot container from Asia to the US West Coast could jump from $2,200 to $6,500 or $9,500+.

Carriers learned between 2023 and 2025 how to defend freight rate floors above $1,800 to $2,000 per 40'HC. They rely on four primary tools:
"""

paras = [p.strip() for p in rewr.split('\n\n') if p.strip()]
for idx, p in enumerate(paras):
    sents = re.split(r'(?<=[.!?])\s+', p)
    last_sent = sents[-1]
    print(f"P{idx+1} Last Sent: {last_sent}")

