import json

title = "SeaRates Weekly Updates: Week 47, 2024"
meta_title = "SeaRates Platform Updates for Week 47, 2024"
meta_description = "Discover the latest SeaRates updates for Week 47, 2024, including tracking updates, new airline support, ship schedules, and LandRates features."

body_markdown = """SeaRates released several tool improvements and platform updates for Week 47, 2024.

## Tracking System Improvements
For the web version, SeaRates updated the Filter and added tooltips displaying shipping line names on carrier logos. Collaboration was also enhanced for Heung-A Shipping, Ignazio Messina, Hoegh Autoliners, and OOCL.

## Air Cargo Tracking Enhancements
Support was added for Azerbaijan Airlines and Air Arabia Abu Dhabi.

## Ship Schedules Updates
Support was added for KambaraKisen, Culines, and Sinokor by Vessel, alongside KambaraKisen by Port.

## Parcel Tracking Improvements
For the API version, autodetect logic was enhanced for requesting.

## Other Updates
- Search Filter: Added a customization option for Button hover color to adjust the search button color.
- FAQ Sections: Added FAQ sections to the Container Tracking, Distance & Time, and Load Calculator pages.
- LandRates.com: Added a Special Offers section to the main page on LandRates.com to compare global land freight rates.

## Announcements
- Calendar tab in the Tracking System tool
- New Version of Route Planner API
- Freight Index 1.0
- Mobile App Version 1.2 with Request System feature
- Load Calculator Version 2.2
- Booking System Version 1.1
- Map platform"""

# Validation checks
assert len(title) <= 60, f"Title length {len(title)} > 60"
assert len(meta_title) <= 60, f"Meta Title length {len(meta_title)} > 60"
assert len(meta_description) <= 155, f"Meta Description length {len(meta_description)} > 155"

for dash in ['—', '–', '--']:
    assert dash not in title, f"Found {dash} in title"
    assert dash not in meta_title, f"Found {dash} in meta_title"
    assert dash not in meta_description, f"Found {dash} in meta_description"
    assert dash not in body_markdown, f"Found {dash} in body_markdown"

result = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_description,
    "body_markdown": body_markdown
}

print(json.dumps(result, indent=2))
