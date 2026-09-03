import json

rewrite_data = {
  "title": "SeaRates Week 12 Updates: New Carrier Tracking Data",
  "meta_title": "SeaRates Week 12 Updates: Tracking API and Carriers",
  "meta_description": "SeaRates adds MTT Shipping, reaching 192 ocean carriers. Explore API updates for vessel AIS data, air freight tracking, and updated ship schedules.",
  "body": "MTT Shipping is now integrated into SeaRates, expanding our container tracking network to 192 ocean lines.\n\nAlong with this integration, we updated our container tracking API to process additional vessel telemetry and real-time vessel tracking data more reliably.\n\nWe also refreshed data exchanges with twelve major carriers: Mediterranean Shipping Company (MSC), Ocean Network Express (ONE), CMA CGM, Turkon, Kuehne + Nagel (KN), Blue Anchor America Line, COSCO, Shipping Corporation of India (SCI), Seaboard Marine, Evergreen, DSV Ocean Transport, and Gold Star Line.\n\n### Air freight and schedule refinements\n\nAir cargo tracking received upgrades this week, focused on LOT Polish Airlines alongside several other carriers. Improving airline data feeds helps maintain consistent supply chain visibility when cargo moves above the clouds.\n\nMeanwhile, our ocean freight schedules tool saw performance adjustments across three search modes.\n\nFor queries by points, we updated feeds from Laurel Navigation, Emirates, AC Container Line, and Interasia Lines.\n\nIf you search schedules by ports, data sources now route smoother for Dong Young, Sinotrans, and CMA CGM.\n\nFinally, vessel-based lookups were refined for Sinotrans, ONE, Ignazio Messina, and Namsung. These ocean carrier integrations keep route planning accurate across different booking workflows."
}

with open("/opt/hermes/profiles/archie/rewrite_step4.json", "w", encoding="utf-8") as f:
    json.dump(rewrite_data, f, ensure_ascii=False, indent=2)

print("Saved rewrite_step4.json")
