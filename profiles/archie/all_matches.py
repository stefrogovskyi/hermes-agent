import re

source_text = """Title: CFS, CY, FTZ, and Bonded Warehouse: Differences and Checklist on Which to Choose? | SeaRates Blog Post

Content:
Knowing the various options available for cargo management is essential for profitable international shipping. Depending on the kind of products and requirements you have, the Container Freight Station (CFS), Container Yard (CY), Foreign Trade Zone (FTZ), and Bonded Warehouse are all key components of the logistics process.
Let’s discover their unique advantages and compare the differences to find the best fit for your shipping needs.

What is CFS (Container Freight Station)?
Do you carry your cargo in a shared container? Here, a Container Freight Station (CFS) is a facility where LCL (Less-than-Container Load) shipments are packed (consolidated) and unpacked (deconsolidated). Before or after your cargo is loaded/unloaded, the shared container is transported via CFS for customs clearance procedures and then for sorting.
CFSs are often located near seaports or airports to rapidly manage cargo before it is shipped or after it arrives.

What is CY (Container Yard)?
A Container Yard (CY) is located in or near seaports/transportation hubs, where FLC (Full Container Load) containers are temporarily stored before or after being loaded onto or unloaded from vessels.
Commonly used for sealed containers that do not require breaking down at terminals. Primarily deals with the physical storage and movement of entire containers, unlike CFS, which is required for cargo consolidating and deconsolidating.

What is an FTZ (Foreign Trade Zone)?
A Foreign Trade Zone (FTZ) is a secure and controlled area for customs duty purposes located within a country or outside the country's customs territory. Used for legitimately deferring/reducing/eliminating customs duties on imported products. Here, goods can be imported, manufactured, processed, and exported with certain customs benefits.
Located near seaports, airports, stations, and transportation hubs. Required for lawful assembly, sorting, or repacking under CBP maintenance.

What is a Bonded Warehouse?
Imported products are stored in a Bonded Warehouse under customs supervision until customs duties, taxes, and other regulations are paid.
Bonded warehouse commodities are “suspended” from customs duties and taxes until they leave the warehouse and enter the domestic market.
International trade enterprises utilize these facilities to manage cash flow, save upfront fees, and overcome complex customs laws. For example:
- United States: Tightly regulated by U.S. Customs and Border Protection (CBP), allowing goods to be stored duty-free until they are imported or re-exported;
- European Union: Allow goods to be stored without paying customs duties or VAT until they are released for consumption or re-exported to a non-EU country;
- United Kingdom: Overseen by HM Revenue and Customs (HMRC), provides the ability to store goods without paying VAT or customs duties until they enter the UK market or are re-exported;
- China: Used to store imported goods with deferred duty payments, and also for good processing, repackaging, or assembling before re-exporting them;
- India: Allow businesses to store imported goods without paying customs duties until they are either cleared for domestic consumption or re-exported;
- Singapore: Managed by the Singapore Customs, offers duty deferral on imported goods and provides businesses with storage solutions for re-exporting or domestic sales, with the benefit of deferred duties.

What’s the difference? Facility roles
CFS: Handles import/export LCL freight | Basic unpacking/packing, light processing | Duties are due upon entry into the domestic market
CY: Stores and stacks FCL containers before and after customs clearance | Most CYs do not process commodities | Duty payment when products leave the yard for consumption
FTZ: Deferred duty imports, manufacturing, processing, and duty-free exports | Duty-free manufacture, assembly, and packaging until goods enter the domestic market | Defer customs charges until goods enter or leave the country
Bonded Warehouse: Stores imported commodities under customs control until tariffs are paid, or they are re-exported | Some processing, packing, and labeling | Defers or eliminates warehouse customs charges until items are freed or re-exported

Typical use cases:
CFS needed for: Consolidations of small shipments from multiple suppliers; Large shipments for distribution need to be deconsolidated; Short-term storage before customs clearance requires handling cargo.
CY needed for: Containers are stored before customs clearance; Short-term goods storage awaiting further transportation; Storing large shipments for export or distribution.
FTZ needed for: Producers and exporters to defer the duties payment on imported goods; Goods are stored for re-export without paying customs duties; Processing, assembly, or packaging without immediate payment of duty.
Bonded warehouse needed for: Storing imported items while waiting for customs clearance; Companies looking for deferring duties until products are on the domestic market; Holding goods for re-export with no duty payment required.

Risk factors to consider:
CFS: Damage risk during handling or deconsolidation; Delays in shipment processing due to congestion; Inventory errors during sorting or packaging.
CY: Container damage due to exposure or lack of security; Long storage times leading to demurrage fees; Logistical delays when containers are not cleared on time.
FTZ: Regulatory changes affecting customs procedures and compliance; Complexity in managing customs duties for goods moving in/out; Over-complication of operational tasks due to multiple layers of compliance.
Bonded Warehouse: Delays caused by incorrect paperwork or incomplete customs documentation; Long-term storage costs leading to increased expenses; Risk of damage or spoilage due to prolonged storage and mismanagement.

Checklist: Which option to choose?
1. What type of goods are you handling? (Small/mixed: CFS; Large/containerized: CY; Processing/manufacturing: FTZ; Long-term/duty deferral: Bonded Warehouse)
2. How urgent is handling and clearance? (Quick/immediate: CFS; Short-term: CY; Processing: FTZ; Long-term/deferred: Bonded Warehouse)
3. Are you processing/assembling? (Basic: CFS; Full processing/manufacturing: FTZ; Some processing: Bonded Warehouse; No processing: CY)
4. Do you need to manage duties and taxes? (Deferring: FTZ/Bonded Warehouse; Immediate: CFS/CY)
5. What are storage needs? (Short-term: CFS/CY; Long-term: FTZ/Bonded Warehouse)"""

rewritten_text = """Title: Choosing CFS, CY, FTZ, or Bonded Warehouse
Meta Title: CFS, CY, FTZ, and Bonded Warehouse Comparison
Meta Description: Compare CFS, CY, FTZ, and bonded warehouses. Learn duty deferral, storage rules, handling risks, and how to choose the right facility for your cargo.

Body:
Cargo routing decides how long cash remains frozen in global transport loops. International shipping relies on four distinct staging facilities: Container Freight Stations, Container Yards, Foreign Trade Zones, and Bonded Warehouses. Each venue handles cargo, duties, and physical movement under different legal frameworks. Matching shipment characteristics to facility capabilities prevents unexpected charges, clearance bottlenecks, and tax liabilities.

## Container Freight Station Mechanics

A Container Freight Station operates near ocean ports or airports. Facilities of this type manage shared container space. Small shipments from multiple suppliers gather here for LCL consolidation and deconsolidation.

Before outbound sailing, workers pack mixed cargo into single containers. Upon inbound arrival, workers unload and sort individual commercial lots before customs clearance. Basic handling includes light processing, unpacking, and repackaging. Customs duties become payable immediately when products pass into the domestic market.

Using a Container Freight Station introduces specific operational hazards:
- Physical damage can occur during manual unpacking or repacking.
- Terminal congestion causes processing delays.
- Sorting mistakes lead to inventory mismatches.

## Container Yard Operations

Container Yards sit within or adjacent to port terminals and transport nodes. These staging sites handle FCL yard storage for whole, sealed ocean boxes.

Unlike freight stations, container yards execute physical stacking and container moves without opening cargo doors. Most yards do not process commodities or break down shipments. Full containers remain stacked awaiting vessel loading or hinterland rail transport. Import tariffs become due when the container leaves the yard perimeter for local domestic distribution.

Storage in container yards involves distinct risks:
- Weather exposure and handling equipment can damage container shells.
- Extended holding times generate steep demurrage charges.
- Customs hold delays disrupt downstream trucking schedules.

## Duty Management via Foreign Trade Zones

A Foreign Trade Zone is a restricted, supervised area treated legally as existing outside national customs territory. Zones sit near ocean ports, airports, and transport hubs.

Operating within these areas unlocks core Foreign Trade Zone benefits. Importers bring raw goods, parts, and finished products into the zone to defer, reduce, or eliminate tariffs. Allowed activities include manufacturing, assembly, processing, sorting, and repacking under customs supervision, including U.S. Customs and Border Protection (CBP) maintenance. Goods exported directly from the zone incur zero domestic import duties. Tariff payments apply only when finished products leave the zone to enter the domestic market. Companies use this import duty deferral strategy to protect working capital during production cycles.

Foreign Trade Zone usage carries clear risks:
- Shifting national trade regulations alter compliance obligations.
- Tracking duty rates for mixed components entering and leaving zones creates administrative complexity.
- Multiple regulatory layers can over-complicate daily warehouse workflows.

## Bonded Warehouse Rules and Jurisdictions

A Bonded Warehouse stores imported commodities under direct customs supervision while tariffs, VAT, and tax obligations remain suspended. These facilities support supply chain tariff optimization by giving enterprises time to clear paperwork, organize re-exports, or sell goods into local channels without paying upfront fees. Some light processing, packing, and labeling occur inside bonded areas.

Customs agencies manage bonded operations under national laws:
- United States: Authorities under U.S. Customs and Border Protection (CBP) enforce strict rules, permitting cargo to remain duty-free prior to formal entry or outward re-shipment.
- European Union: Shipments remain exempt from import tariffs and VAT until declared for local consumption or shipped outside member territory.
- United Kingdom: Rules enforced by HM Revenue and Customs (HMRC) let traders store commercial stock free of VAT or import levies until released domestically or re-exported.
- China: Facilities hold foreign freight under duty suspension, permitting secondary assembly, repackaging, or physical processing before foreign re-export.
- India: Commercial enterprises retain imported merchandise tariff-free until finalizing clearance for internal consumption or foreign re-export.
- Singapore: Direct supervision by Singapore Customs provides flexible storage choices and deferred tax schedules for domestic placement or regional re-export.

Bonded warehouse customs compliance requires attention to specific operational risks:
- Incomplete documentation or incorrect paperwork triggers customs delays.
- Prolonged holding times accumulate high storage fees.
- Mismanaged storage conditions risk product damage or spoilage.

## Selection Checklist

Choosing the right logistics facility depends on five operational factors.

### 1. Shipment Structure
- Small or mixed commercial lots needing packing or breakdown require a Container Freight Station for LCL consolidation and deconsolidation.
- Sealed, full container loads needing pre-clearance holding require FCL yard storage in a Container Yard.
- Raw materials or parts requiring assembly, manufacturing, or processing alongside duty deferral require a Foreign Trade Zone.
- Commercial imports requiring extended storage, duty deferral, or pending re-export require a Bonded Warehouse.

### 2. Processing Requirements
- Basic handling limited to unpacking and packing: Container Freight Station.
- Full manufacturing, industrial processing, or product assembly: Foreign Trade Zone.
- Secondary packaging, labeling, or light touch-ups: Bonded Warehouse.
- Zero processing or cargo opening: Container Yard.

### 3. Clearance and Duty Strategy
- Immediate duty settlement upon domestic entry: Container Freight Station or Container Yard.
- Duty deferral, reduction, or elimination on imports and re-exports: Foreign Trade Zone or Bonded Warehouse.

### 4. Turnaround Urgency
- Rapid cargo sorting and immediate dispatch: Container Freight Station.
- Short-term staging before onward transport or clearance: Container Yard.
- Industrial assembly runs combined with deferred duties: Foreign Trade Zone.
- Extended holding periods prior to final clearance or export: Bonded Warehouse.

### 5. Storage Duration
- Short-term storage prior to shipping or domestic pickup: Container Freight Station or Container Yard.
- Long-term storage paired with customs clearance management: Foreign Trade Zone or Bonded Warehouse."""

def clean_tokens(text):
    return re.findall(r'\b[\w\'-]+\b', text.lower())

src_words = clean_tokens(source_text)
rew_words = clean_tokens(rewritten_text)

# Find all consecutive matches >= 4
matches = []
for i in range(len(rew_words)):
    for j in range(len(src_words)):
        k = 0
        while i + k < len(rew_words) and j + k < len(src_words) and rew_words[i+k] == src_words[j+k]:
            k += 1
        if k >= 4:
            phrase = " ".join(rew_words[i:i+k])
            matches.append((k, phrase, i, j))

# Filter overlapping sub-matches
unique_matches = {}
for k, phrase, i, j in sorted(matches, key=lambda x: x[0], reverse=True):
    # check if subphrase of already seen match
    already_seen = False
    for existing in unique_matches:
        if phrase in existing:
            already_seen = True
            break
    if not already_seen:
        unique_matches[phrase] = k

print("--- All Matches >= 4 words ---")
for phrase, k in sorted(unique_matches.items(), key=lambda x: x[1], reverse=True):
    print(f"{k} words: '{phrase}'")
