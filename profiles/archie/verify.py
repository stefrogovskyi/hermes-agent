import json
import re

title = "SeaRates Weekly Platform Updates: Week 34 Highlights"
meta_title = "SeaRates Week 34 Updates: New Features & Upgrades"
meta_description = "Discover SeaRates Week 34 updates: Load Calculator V2, Air Cargo Tracking additions, Tracking API enhancements, and newly released platform features."

body = """The SeaRates team appreciates your continued trust and support. We consistently upgrade our platform capabilities to deliver superior service, and we are excited to showcase our latest weekly advancements designed to elevate your logistics workflows. To stay fully informed on our recent progress, feel free to review our prior release notes.

In our Week 34 releases, we introduced Version 2 of the Load Calculator web application. This update refines the internal packing algorithms for arranging boxed items and piping cargo inside trucks or freight containers. Users can now inspect step-by-step cargo arrangement plans by downloading a PDF document directly through their web browser. For air freight logistics, we expanded air cargo tracking coverage to 5 additional carriers: SAC South American Airways, Wizz Air, FITS Aviation, Cayman Airways, alongside Iran Air. Furthermore, integration responsiveness was optimized for Southwest Airlines, Delta Air Lines, Qatar Airways, and Batik Air.

Our shipment tracking services received significant upgrades this week as well. Query functionality within the Tracking History API now captures complete shipment records across both BL and BK identifiers. On the provider front, operational performance was enhanced across a wide range of partners: Dachser, Sinokor, CMA CGM, Hapag-Lloyd, Swire Shipping, DHL Global Forwarding, Meratus Line, Westwood Shipping Lines, Kuehne + Nagel (KN), Jin Jiang Shipping (SHJJ), Emirates Shipping Line, Reel Shipping FZCO, Hai Hua Shipping (HASCO), and Evergreen. Meanwhile, our Freight Index tool features refined route-level calculation formulas and a clearer presentation of historical pricing requests. On mobile, iOS application users can now authenticate seamlessly via Google accounts or direct internal sign-in without requiring a redirect to the main SeaRates website. To streamline service pricing inquiries, our IT Quote Request form now supports selections for Parcel Tracking API access, Enterprise Web integration, Mobile App Web connections, Parcel Tracking Web interface, and Parcel Tracking Web access.

Additionally, we published dedicated web pages for the Parcel Tracking API alongside Distance & Time tools, while updating the layout and informative content across the IMO Classes page.

Newly Released Platform Features:
- Booking System (v1.1)
- Rail Tracking API interface
- Load Calculator (v2.2)
- Map platform services
- Mobile App (v1.2 featuring the Request System)
- Parcel Tracking API
- Geocoding API and Autocomplete service (v0.8)
- Route Planner API new edition
- Dedicated 'Transport' tab within Logistics Map
- Freight Index (v1.0)"""

data = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_description,
    "body": body
}

print(json.dumps(data, indent=2))
