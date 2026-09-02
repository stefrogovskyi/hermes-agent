---
name: tradingeconomics-commodity-quotes
description: Use to get live commodity prices from Trading Economics.
---

# Trading Economics Commodity Market Intelligence

Workflow and tools for fetching real-time commodity spot/futures prices, unit specifications, daily/monthly percentage changes, all-time high/low ranges, and comprehensive catalog breakdown from Trading Economics (`tradingeconomics.com`).

## Trigger Conditions
Use when:
- The user asks for the current price, quote, or trend of any commodity (e.g. Sugar, Wheat, Soybeans, Crude Oil, Natural Gas, Gold, Copper, Coffee, Cocoa, Rubber, Lumber, etc.).
- Salvage pricing or valuation of abandoned/unclaimed cargo lots requires benchmark commodity market rates.
- Comparing port cargo inventory against global commodity index fluctuations.

## Key Principles & Execution

1. **Instant Direct Real-Time Scraper (`get_commodity_price.py`)**
   - Execute `/opt/hermes/scripts/get_commodity_price.py "<commodity_name_or_slug>"` to obtain clean JSON data.
   - Automatically supports English & Russian commodity names (e.g. `сахар` ➔ `sugar`, `золото` ➔ `gold`, `нефть` ➔ `crude-oil`, `пшеница` ➔ `wheat`).
   - Returns:
     * `price`: Exact live market quote.
     * `unit`: Trading unit (e.g. `Cents/LB`, `USD/BBL`, `USD/t oz.`, `USD/MT`, `USd/Bu`).
     * `day_change` & `pct_change`: Daily dollar and percentage delta.
     * `previous_close`, `all_time_high`, `all_time_low`, `historical_range`.

2. **Full Commodity Catalog Reference**
   - Main categories covered:
     * **Agricultural**: Sugar, Wheat, Soybeans, Corn, Coffee, Cocoa, Cotton, Palm Oil, Rice, Canola, Orange Juice, Tea, Wool.
     * **Energy**: Crude Oil, Brent, Natural Gas, Gasoline, Heating Oil, Coal, Uranium, TTF Gas, UK Gas.
     * **Metals**: Gold, Silver, Platinum, Palladium, Copper, Aluminum, Zinc, Nickel, Lead, Tin, Lithium, Cobalt, Magnesium.
     * **Industrial**: Steel, Iron Ore, Rebar, Bitumen, Rubber, Soda Ash, Lumber, Polysilicon, Kraft Pulp.
     * **Livestock**: Live Cattle, Feeder Cattle, Lean Hogs, Milk, Cheese, Butter.
     * **Indexes & Carbon**: CRB Index, Rogers Raw Materials, Carbon Emissions (EUA), UK/EU Electricity.
   - Offline catalog cache is stored at `/root/commodities_catalog.json`.

3. **Fallback to Headless Browser / Playwright**
   - If Trading Economics enables interactive Cloudflare challenges or dynamic JavaScript hydration updates, trigger `browser_exec` or Playwright via headless Chrome CDP.

## CLI Usage Example
```bash
python3 /opt/hermes/scripts/get_commodity_price.py sugar
python3 /opt/hermes/scripts/get_commodity_price.py "пшеница"
python3 /opt/hermes/scripts/get_commodity_price.py "crude-oil"
```
