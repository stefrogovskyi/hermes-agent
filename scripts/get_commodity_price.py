#!/usr/bin/env python3
"""
Trading Economics Live Commodity Price Extractor
Fetches real-time market data, units, changes, and historical range for any commodity.
"""

import sys
import json
import urllib.request
import urllib.error
import re
from bs4 import BeautifulSoup

COMMODITY_ALIASES = {
    # Russian aliases
    "сахар": "sugar",
    "сахар-сырец": "sugar",
    "пшеница": "wheat",
    "кукуруза": "corn",
    "соя": "soybeans",
    "соевые бобы": "soybeans",
    "кофе": "coffee",
    "какао": "cocoa",
    "хлопок": "cotton",
    "пальмовое масло": "palm-oil",
    "рапс": "canola",
    "рис": "rice",
    "нефть": "crude-oil",
    "брент": "brent-crude-oil",
    "газ": "natural-gas",
    "золото": "gold",
    "серебро": "silver",
    "медь": "copper",
    "алюминий": "aluminum",
    "никель": "nickel",
    "цинк": "zinc",
    "свинец": "lead",
    "олово": "tin",
    "литий": "lithium",
    "уголь": "coal",
    "сталь": "steel",
    "железная руда": "iron-ore",
    "древесина": "lumber",
    "пиломатериалы": "lumber",
    "каучук": "rubber",
    "молоко": "milk",
    "сыр": "cheese",
    "масло": "butter",
    "крупный рогатый скот": "live-cattle",
    "свинина": "lean-hogs",
    # English aliases
    "crude": "crude-oil",
    "oil": "crude-oil",
    "brent": "brent-crude-oil",
    "gas": "natural-gas",
    "natgas": "natural-gas"
}

def resolve_slug(query: str) -> str:
    cleaned = query.strip().lower()
    if cleaned in COMMODITY_ALIASES:
        return COMMODITY_ALIASES[cleaned]
    # Replace spaces with hyphens
    slug = re.sub(r"[^\w\s-]", "", cleaned).strip().replace(" ", "-")
    return slug

def fetch_commodity(query: str) -> dict:
    slug = resolve_slug(query)
    url = f"https://tradingeconomics.com/commodity/{slug}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return {"success": False, "error": f"Commodity '{query}' (slug '{slug}') not found on Trading Economics (404).", "url": url}
        return {"success": False, "error": f"HTTP {e.code}: {e.reason}", "url": url}
    except Exception as e:
        return {"success": False, "error": str(e), "url": url}
        
    soup = BeautifulSoup(html, "html.parser")
    
    # Extract page title
    title_tag = soup.find("title")
    title = title_tag.text.strip() if title_tag else f"{slug.title()} Commodity Price"
    commodity_name = title.split("-")[0].strip() if "-" in title else slug.title()
    
    # Extract primary price elements
    price_tag = soup.find("span", id="market_last") or soup.find("div", id="market_last")
    price = price_tag.text.strip() if price_tag else "N/A"
    
    day_chg_tag = soup.find("span", id="market_daily_chg")
    day_chg = day_chg_tag.text.strip() if day_chg_tag else "N/A"
    
    pct_chg_tag = soup.find("span", id="market_daily_Pchg")
    pct_chg = pct_chg_tag.text.strip() if pct_chg_tag else "N/A"
    
    # Extract stats from overview table
    unit = "N/A"
    prev_price = "N/A"
    highest = "N/A"
    lowest = "N/A"
    dates_range = "N/A"
    frequency = "N/A"
    
    tables = soup.find_all("table")
    for t in tables:
        rows = t.find_all("tr")
        for r in rows:
            tds = [td.text.strip() for td in r.find_all(["th", "td"])]
            if len(tds) >= 7 and ("Actual" in tds or "Unit" in tds):
                continue
            # Look for the row with data
            if len(tds) >= 7:
                # Format: ['', '18.38', '17.81', '65.20', '1.25', '1912 - 2026', 'Cents/LB', 'Daily', '']
                vals = [x for x in tds if x]
                if len(vals) >= 6:
                    prev_price = vals[1] if len(vals) > 1 else "N/A"
                    highest = vals[2] if len(vals) > 2 else "N/A"
                    lowest = vals[3] if len(vals) > 3 else "N/A"
                    dates_range = vals[4] if len(vals) > 4 else "N/A"
                    unit = vals[5] if len(vals) > 5 else "N/A"
                    frequency = vals[6] if len(vals) > 6 else "N/A"
                    break

    return {
        "success": True,
        "query": query,
        "name": commodity_name,
        "slug": slug,
        "price": price,
        "unit": unit,
        "day_change": day_chg,
        "pct_change": pct_chg,
        "previous_close": prev_price,
        "all_time_high": highest,
        "all_time_low": lowest,
        "historical_range": dates_range,
        "frequency": frequency,
        "url": url
    }

if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "sugar"
    result = fetch_commodity(q)
    print(json.dumps(result, ensure_ascii=False, indent=2))
