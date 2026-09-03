# Mapping claims from Draft Rewrite to Original Source Text

draft_claims = [
    ("Title & Meta", "SeaRates Release Notes: Week 37 2024 Platform Updates / Tools and API Changes"),
    ("Meta Desc", "add a Transport tab to the Logistics Map, improve container load optimization, and expand multi-carrier tracking integration"),
    ("Intro P1", "SeaRates expanded booking visibility across road transit"),
    ("Intro P1", "refreshed tracking connectors while tweaking spatial calculations inside loading tools"),
    ("Transport 1", "A new Transport tab transforms the interface into a functional logistics map transport directory."),
    ("Transport 2", "Users can now browse transport units ready for booking, viewing specific equipment types, vehicle models, current locations, target destinations, rate quotes, and availability dates."),
    ("Transport 3", "Data renders simultaneously in list view and on map pins."),
    ("Transport 4", "Selecting an entry opens detailed vehicle cards, where filters allow users to narrow results by location, vehicle type, or price range."),
    ("Transport 5", "Standard sharing links let teams copy exact unit listings."),
    ("Transport 6", "If a haulage scenario requires tailored setup, shippers can submit packing requests with specific routes and budget limits, or start a direct chat with account managers."),
    ("Carrier 1", "Air cargo tracking now includes deeper data feeds from Air France."),
    ("Carrier 2", "Maritime tracking underwent updates to refine multi-carrier tracking integration across lines including OOCL, Asyad Line, CMA CGM, Sarjak Container Lines, Maersk, Akkon Lines, Atlantic Container Line (ACL), and Grimaldi Deep Sea S.P.A."),
    ("Carrier 3", "On the web interface, shipment cards now feature a Follow button for one-click transfers into the main Dashboard."),
    ("Carrier 4", "Navigation additions include new menu items for parcel tracking API integration and Parcel Tracking Web. Explanatory content was refreshed on Container Tracking, Tracking System API, and For Carriers pages. SeaRates launched a Quotation System landing page. Airline vendor listings went live on AirRates.com, paired with new railway operator directories on LandRates.com to expand coverage across transport modes."),
    ("Schedules 1", "Searching vessel schedules by ship name now supports Pacific International Lines (PIL)."),
    ("Schedules 2", "For heavy cargo and rolling stock, Ro-Ro vessel schedules under Wallenius Wilhelmsen and Sallaum Lines now process point-to-point route searches."),
    ("Load Calc 1", "Updates to container load optimization focus on practical loading parameters. The web calculator sets Height as a default third dimension under the Spacing settings tab."),
    ("Load Calc 2", "Cargo orientation control now includes Length and Width marks with selection checkboxes to flip box positioning."),
    ("Load Calc 3", "For full container loads containing uniform box dimensions, the step-by-step loading algorithm was revised to render cleaner cargo placement sequences."),
    ("Pipeline 1", "Upcoming builds will introduce web features for air tracking, Geocoding API autocomplete v0.8, a new Route Planner API release, and Freight Index 1.0."),
    ("Pipeline 2", "Development continues on mobile app v1.2 with request integration, Load Calculator v2.2, Booking System v1.1, a dedicated real-time freight tracking API, rail tracking on LandRates.com, and a unified web tracking interface.")
]

print("Fact Check Analysis:")
for loc, claim in draft_claims:
    print(f"\n[{loc}] Claim:\n  '{claim}'")
