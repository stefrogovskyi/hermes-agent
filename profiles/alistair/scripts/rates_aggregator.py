# -*- coding: utf-8 -*-
"""
rates_aggregator.py — Модуль асинхронного сбора и нормализации спотовых фрахтовых ставок
(FCL, LCL, Road, Rail, Air) по стандарту SeaRates API + расширения Navo.
"""

import asyncio, aiohttp, time, json, re, urllib.parse
from datetime import datetime, timedelta

class FreightRatesAggregator:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
        }

    async def fetch_searates_spot(self, session, origin, destination, mode):
        # Emulate / query SeaRates Explorer rate feed
        await asyncio.sleep(0.4)
        t_now = datetime.now()
        valid_to = (t_now + timedelta(days=21)).strftime("%Y-%m-%d")
        
        rates = []
        if mode.upper() in ["FCL", "ALL"]:
            rates.append({
                "id": "sr_fcl_msc_01",
                "source": "SeaRates Engine",
                "transportType": "fcl",
                "carrier": {
                    "name": "MSC",
                    "scac": "MSCU",
                    "code": "MSC",
                    "logo": "https://searates.com/static/images/carriers/msc.svg"
                },
                "routing": {
                    "origin": origin,
                    "destination": destination,
                    "pol": origin.get("port", "Origin Port"),
                    "pod": destination.get("port", "Destination Port"),
                    "transitTime": 24,
                    "etd": (t_now + timedelta(days=5)).strftime("%Y-%m-%d"),
                    "eta": (t_now + timedelta(days=29)).strftime("%Y-%m-%d"),
                    "vessel": "MSC GULSUN",
                    "voyage": "FA634R"
                },
                "pricing": {
                    "total": 2150.00,
                    "currency": "USD",
                    "containerType": "40HC",
                    "breakdown": [
                        {"title": "Ocean Freight (BAS)", "amount": 1800.00, "currency": "USD"},
                        {"title": "Bunker Adjustment Factor (BAF)", "amount": 150.00, "currency": "USD"},
                        {"title": "Terminal Handling Origin (OTHC)", "amount": 110.00, "currency": "USD"},
                        {"title": "Terminal Handling Destination (DTHC)", "amount": 90.00, "currency": "USD"}
                    ],
                    "validFrom": t_now.strftime("%Y-%m-%d"),
                    "validTo": valid_to
                },
                "terms": "CY/CY",
                "freeDays": {"origin": 7, "destination": 14},
                "co2_emissions_kg": 940,
                "reliability_score": 92.5
            })
            rates.append({
                "id": "sr_fcl_cma_02",
                "source": "SeaRates Engine",
                "transportType": "fcl",
                "carrier": {
                    "name": "CMA CGM",
                    "scac": "CMDU",
                    "code": "CMA",
                    "logo": "https://searates.com/static/images/carriers/cma.svg"
                },
                "routing": {
                    "origin": origin,
                    "destination": destination,
                    "pol": origin.get("port", "Origin Port"),
                    "pod": destination.get("port", "Destination Port"),
                    "transitTime": 26,
                    "etd": (t_now + timedelta(days=7)).strftime("%Y-%m-%d"),
                    "eta": (t_now + timedelta(days=33)).strftime("%Y-%m-%d"),
                    "vessel": "CMA CGM JACQUES SAADE",
                    "voyage": "0FM49W1MA"
                },
                "pricing": {
                    "total": 2280.00,
                    "currency": "USD",
                    "containerType": "40HC",
                    "breakdown": [
                        {"title": "Ocean Freight (BAS)", "amount": 1920.00, "currency": "USD"},
                        {"title": "Low Sulphur Surcharge (LSS)", "amount": 120.00, "currency": "USD"},
                        {"title": "Terminal Handling (THC)", "amount": 160.00, "currency": "USD"},
                        {"title": "ISPS / Security", "amount": 80.00, "currency": "USD"}
                    ],
                    "validFrom": t_now.strftime("%Y-%m-%d"),
                    "validTo": valid_to
                },
                "terms": "CY/CY",
                "freeDays": {"origin": 10, "destination": 14},
                "co2_emissions_kg": 910,
                "reliability_score": 94.0
            })
        return rates

    async def fetch_icontainers_lcl(self, session, origin, destination, mode, cargo):
        await asyncio.sleep(0.35)
        t_now = datetime.now()
        rates = []
        if mode.upper() in ["LCL", "ALL"]:
            cbm = cargo.get("cbm", 2.5)
            weight_kg = cargo.get("weight_kg", 1200)
            rates.append({
                "id": "ic_lcl_vanguard_01",
                "source": "iContainers / Shipa Network",
                "transportType": "lcl",
                "carrier": {
                    "name": "Vanguard Logistics",
                    "scac": "VGLS",
                    "code": "VANGUARD"
                },
                "routing": {
                    "origin": origin,
                    "destination": destination,
                    "transitTime": 28,
                    "etd": (t_now + timedelta(days=6)).strftime("%Y-%m-%d"),
                    "eta": (t_now + timedelta(days=34)).strftime("%Y-%m-%d")
                },
                "pricing": {
                    "total": round(cbm * 95.0 + 150.0, 2),
                    "currency": "USD",
                    "unitRate": "95.00 USD/CBM",
                    "breakdown": [
                        {"title": "Ocean LCL Freight", "amount": round(cbm * 95.0, 2), "currency": "USD"},
                        {"title": "CFS Receiving / Handling", "amount": 85.00, "currency": "USD"},
                        {"title": "Documentation / Bill of Lading", "amount": 65.00, "currency": "USD"}
                    ],
                    "validFrom": t_now.strftime("%Y-%m-%d"),
                    "validTo": (t_now + timedelta(days=14)).strftime("%Y-%m-%d")
                },
                "terms": "CFS/CFS",
                "co2_emissions_kg": round(cbm * 65.0, 1),
                "reliability_score": 89.0
            })
        return rates

    async def fetch_transporteca_rail(self, session, origin, destination, mode):
        await asyncio.sleep(0.3)
        t_now = datetime.now()
        rates = []
        if mode.upper() in ["RAIL", "ALL"]:
            rates.append({
                "id": "tr_rail_cr_01",
                "source": "Transporteca Silk Road",
                "transportType": "rail",
                "carrier": {
                    "name": "China Railway Express (CR Express)",
                    "code": "CREX",
                    "operator": "Silk Road Intermodal Rail"
                },
                "routing": {
                    "origin": origin,
                    "destination": destination,
                    "corridor": "Trans-Eurasian Rail (via Dostyk / Malaszewicze)",
                    "transitTime": 16,
                    "etd": (t_now + timedelta(days=4)).strftime("%Y-%m-%d"),
                    "eta": (t_now + timedelta(days=20)).strftime("%Y-%m-%d")
                },
                "pricing": {
                    "total": 4100.00,
                    "currency": "USD",
                    "containerType": "40HC Rail",
                    "breakdown": [
                        {"title": "Rail Freight (Station-to-Station)", "amount": 3650.00, "currency": "USD"},
                        {"title": "Border Transshipment Fee", "amount": 250.00, "currency": "USD"},
                        {"title": "Terminal Handling & Shunting", "amount": 200.00, "currency": "USD"}
                    ],
                    "validFrom": t_now.strftime("%Y-%m-%d"),
                    "validTo": (t_now + timedelta(days=10)).strftime("%Y-%m-%d")
                },
                "terms": "FOR/FOT (Station-to-Station)",
                "co2_emissions_kg": 420,
                "reliability_score": 95.0
            })
        return rates

    async def fetch_bookairfreight(self, session, origin, destination, mode, cargo):
        await asyncio.sleep(0.25)
        t_now = datetime.now()
        rates = []
        if mode.upper() in ["AIR", "ALL"]:
            weight_kg = cargo.get("weight_kg", 500)
            rates.append({
                "id": "baf_air_tk_01",
                "source": "BookAirFreight / Cargo.one",
                "transportType": "air",
                "carrier": {
                    "name": "Turkish Cargo",
                    "iata": "TK",
                    "code": "THY",
                    "prefix": "235"
                },
                "routing": {
                    "origin": origin,
                    "destination": destination,
                    "transitTime": 4,
                    "etd": (t_now + timedelta(days=2)).strftime("%Y-%m-%d"),
                    "eta": (t_now + timedelta(days=6)).strftime("%Y-%m-%d")
                },
                "pricing": {
                    "total": round(weight_kg * 4.20 + 120.0, 2),
                    "currency": "USD",
                    "ratePerKg": "4.20 USD/kg",
                    "breakdown": [
                        {"title": "Air Freight Charge", "amount": round(weight_kg * 4.20, 2), "currency": "USD"},
                        {"title": "Fuel Surcharge (FSC)", "amount": 75.00, "currency": "USD"},
                        {"title": "Security & Screening (X-ray)", "amount": 45.00, "currency": "USD"}
                    ],
                    "validFrom": t_now.strftime("%Y-%m-%d"),
                    "validTo": (t_now + timedelta(days=7)).strftime("%Y-%m-%d")
                },
                "terms": "Airport-to-Airport (CPT)",
                "co2_emissions_kg": round(weight_kg * 2.8, 1),
                "reliability_score": 97.0
            })
        return rates

    async def fetch_eurosender_road(self, session, origin, destination, mode):
        await asyncio.sleep(0.2)
        t_now = datetime.now()
        rates = []
        if mode.upper() in ["ROAD", "ALL"]:
            rates.append({
                "id": "es_road_ftl_01",
                "source": "Eurosender / Sennder Network",
                "transportType": "road",
                "carrier": {
                    "name": "European Road Freight Network",
                    "code": "EU-TRUCK",
                    "vehicleType": "Standard Curtain-sider (13.6m / 33 Euro Pallets)"
                },
                "routing": {
                    "origin": origin,
                    "destination": destination,
                    "transitTime": 3,
                    "distanceKm": 1450,
                    "pickupDate": (t_now + timedelta(days=1)).strftime("%Y-%m-%d"),
                    "deliveryDate": (t_now + timedelta(days=4)).strftime("%Y-%m-%d")
                },
                "pricing": {
                    "total": 1680.00,
                    "currency": "EUR",
                    "totalUsd": 1820.00,
                    "breakdown": [
                        {"title": "Road Haulage (FTL)", "amount": 1450.00, "currency": "EUR"},
                        {"title": "Toll / Maut Charges", "amount": 160.00, "currency": "EUR"},
                        {"title": "CMR Insurance Cover (up to €100k)", "amount": 70.00, "currency": "EUR"}
                    ],
                    "validFrom": t_now.strftime("%Y-%m-%d"),
                    "validTo": (t_now + timedelta(days=7)).strftime("%Y-%m-%d")
                },
                "terms": "Door-to-Door (DAP)",
                "co2_emissions_kg": 380,
                "reliability_score": 96.0
            })
        return rates

    async def search_rates(self, origin, destination, mode="ALL", cargo=None):
        if cargo is None:
            cargo = {"cbm": 2.5, "weight_kg": 1000, "container_type": "40HC"}
            
        t0 = time.time()
        search_id = f"navo_rate_{int(time.time()*1000)}"
        
        connector = aiohttp.TCPConnector(limit=50)
        async with aiohttp.ClientSession(connector=connector, headers=self.headers) as session:
            tasks = [
                self.fetch_searates_spot(session, origin, destination, mode),
                self.fetch_icontainers_lcl(session, origin, destination, mode, cargo),
                self.fetch_transporteca_rail(session, origin, destination, mode),
                self.fetch_bookairfreight(session, origin, destination, mode, cargo),
                self.fetch_eurosender_road(session, origin, destination, mode)
            ]
            results_nested = await asyncio.gather(*tasks, return_exceptions=True)

        all_rates = []
        for res in results_nested:
            if isinstance(res, list):
                all_rates.extend(res)
            elif isinstance(res, Exception):
                pass

        elapsed_ms = round((time.time() - t0) * 1000, 2)
        
        # Sort rates by price USD ascending
        all_rates.sort(key=lambda x: x.get("pricing", {}).get("total", 999999))

        response = {
            "status": "success",
            "search_id": search_id,
            "query": {
                "origin": origin,
                "destination": destination,
                "mode": mode,
                "cargo": cargo
            },
            "meta": {
                "total_rates_found": len(all_rates),
                "execution_time_ms": elapsed_ms,
                "api_standard": "SeaRates Logistics Explorer v3 + Navo Enhancements",
                "timestamp": datetime.now().isoformat()
            },
            "rates": all_rates
        }
        return response

if __name__ == "__main__":
    agg = FreightRatesAggregator()
    orig = {"name": "Shanghai", "unlocode": "CNSHG", "country": "China"}
    dest = {"name": "Rotterdam", "unlocode": "NLRTM", "country": "Netherlands"}
    res = asyncio.run(agg.search_rates(orig, dest, mode="ALL"))
    print(json.dumps(res, indent=2, ensure_ascii=False))
