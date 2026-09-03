from audit_script import original, candidate

# Air carriers 33 list
air_33_orig = ["Aercaribe", "CMA CGM Air Cargo", "Evelop Airlines", "Icelandair", "Kam Air", "Stabo Air Limited", "SunClass Airlines", "Hong Kong Airlines", "Airlink", "Binter Canarias", "Hainan Airlines", "RwandAir", "Tianjin Airlines", "West Air", "Yemen Airways", "Air Tahiti Nui", "Laparkan Airways", "Norse Atlantic Airways", "Transportes Aereos Bolivianos", "YTO Cargo Airlines", "Cayman Airways", "FITS Aviation", "Iran Air", "SAC South American Airways", "Wizz Air", "Air Madagascar", "LAM Mozambique Airlines", "Nauru Airlines", "Air Austral", "MIAT Mongolian Airlines", "US-Bangla Airlines", "Canadian North", "Global Air"]

for name in air_33_orig:
    if name not in candidate:
        print("Missing air carrier in Candidate:", name)

# Air carriers 20 list
air_20_orig = ["Kuwait Airways", "Suparna Airlines", "DHL Aviation", "Air New Zealand", "Cathay Pacific Airways", "Saudi", "Allied Air", "El Al Israel Airlines", "Batik Air", "Qatar Airways", "Delta Airlines", "SouthWest Airlines", "Atlas Air", "Singapore Airlines", "United Airlines", "Finnair", "Emirates", "TAP Portugal", "Air China Cargo", "Air India"]

for name in air_20_orig:
    if name not in candidate:
        print("Missing air provider in Candidate:", name)

# Ocean 4 list
ocean_4_orig = ["Safetrans Line", "M-Line", "Reel Shipping FZCO", "Hub Shipping"]
for name in ocean_4_orig:
    if name not in candidate:
        print("Missing ocean 4 in Candidate:", name)

# Ocean 32 list
ocean_32_orig = ["ECU Worldwide", "CMA CGM", "ZIM", "Yang Ming", "Avana Global FZCO (BALAJI)", "Evergreen", "W.E.C. (West European Container) Lines", "Hyundai Merchant Marine (HMM)", "Hapag-Lloyd", "Shipco Transport", "Orient Overseas Container Line (OOCL)", "Jin Jiang Shipping (SHJJ)", "Swire Shipping", "Atlantic Container Line (ACL)", "TransContainer", "Aladin Express", "NewStar", "Hellmann Worldwide Logistics", "Turkon", "Geodis Ocean", "Reel Shipping FZCO", "Sinokor", "Kuehne + Nagel (KN)", "Westwood Shipping Lines", "Hai Hua Shipping (HASCO)", "DHL Global Forwarding", "Dachser", "Emirates Shipping Line", "Meratus Line", "Pan Continental Shipping", "Ocean Network Express (ONE)", "COSCO"]

for name in ocean_32_orig:
    if name not in candidate:
        print("Missing ocean 32 in Candidate:", name)

print("Carrier lists check complete.")
