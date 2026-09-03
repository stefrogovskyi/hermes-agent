import re

orig = """Is it possible to manage project cargo at a container terminal and ship it by container vessel without disrupting schedules or causing operational complications? The Port of Brisbane proves that this is possible, as 15 yachts were loaded from the quay and from the water onto the CMA CGM Abu Dhabi vessel, while containers continued to move.

There was no panic caused by uncertainty, but rather a consistent plan: deck planning that ensures the ship's stability, lift control, a sequence that does not interfere with container operations, and marine fastenings that leave no room for swaying.

Consolidating such high-value cargo on a regular service line can beat the Ro-Ro/HL price and offer shorter transit time. So, let's break down this case step by step.

The Myth we’re busting: “Project cargo and container terminals don’t mix.”
So, how were 15 motor yachts transported without causing bottlenecks in traffic areas? The answer is planning. This operation is a prime example of careful management, from fencing off the project area on deck and limiting crane operating times to controlling hybrid lifts (from the pier and water). Don't rely solely on improvisation. Then this myth will have no bearing on your logistics.
Safety in this area was strict. Surveys were also conducted with verified lifting points, jointly developed fastenings, and appropriate fastenings.

Case snapshot: one container ship, 15 yachts. Wasn’t a routine call.
CMA CGM Abu Dhabi, a > 15,000-TEU ship (about 366 m long and 51 m wide), took on an unusual deck mix while box work continued nearby. Namely, 15 recreational yachts were loaded in a single call at the Port of Brisbane, Australia.
The operation combined two methods: yachts were lifted from the quay and directly from floating units alongside, a hybrid setup that shortened the turnaround and kept risk under control.
What made it unique? It was the largest single shipment of yachts ever transported on a container vessel. Parallel handling of standard containers and a breakbulk deck of yachts, with lifts from shore and from the water executed inside tight weather/tide windows.
Stakeholders: The carrier CMA CGM, Port of Brisbane/terminal teams, and specialized crane operators coordinating a dedicated project workflow on deck.

How do you load yachts on a container ship?
1) Plan your work in advance: deck and stability. Determine where each yacht will sit and arrival order. Check weight, center of gravity, windage, vessel stability limits.
2) Deck preparation: Clear project area, install cradles or steel beds for each hull, lay down protective mats for contact between metal and paint.
3) Select best rigging gear: Measure crane radius and lifting capacity, select slings and spreaders matching lifting points, pad straps so gelcoat is protected.
4) Run hybrid lifts: From quay (low-loaders, lift into cradle) and from water (bring alongside, slings, lift during weather/tide windows).
5) Plan loading sequence on deck: Coordinate crane times with container movement to prevent idle time.
6) Fastening and lashing: Fix in place with wedges, supports, chains at designated points, welded deck fastenings where needed.
7) Finalize paperwork: Pre-loading inspections, photos, cargo plan updates, insurance confirmations, shipping documents.

Container ship vs. heavy-lift or Ro-Ro:
Container Ship: High fixed frequency, predictable ETAs, strong cost efficiency via consolidation, requires deck planning, best for batches (15 yachts) and show seasons.
Heavy-Lift (MPP/HL): Irregular/spot, variable reliability, good for single OOG, flexible height/deck limits.
Ro-Ro: Medium frequency, good reliability on limited routes, good if drivable, ramp/height limits.

Safety and risk control for high-value cargo:
1) Respect weather conditions and stop lifting if weather deteriorates.
2) Protect hull gelcoat over schedule: pad straps, pre-tension test.
3) 100% lashing safety: supports, chains, welded stoppers; re-check before departure.
4) Insurance & pre-load photo survey: record hull/drives/electronics condition and certificates.

Conclusion:
High-value breakbulk cargo can move on regular container vessels without schedule disruption. Consolidating on container lines beats Ro-Ro/HL pricing and transit times. Contact sales@searates.com for custom logistics solutions."""

draft = """Title: Loading 15 Yachts on a 15,000 TEU Ship at Brisbane
Meta-Title: Loading 15 Yachts on a 15,000 TEU Ship at Brisbane
Meta-Description: Port of Brisbane loaded 15 yachts onto CMA CGM Abu Dhabi without delays. How hybrid lifts and deck planning make yacht transport logistics work.

# Main Article Content

Heavy cargo on a scheduled liner always breeds nervousness on the quay.

When the 366-meter CMA CGM Abu Dhabi tied up at the Port of Brisbane, terminal crews had to load 15 recreational motor yachts onto its deck without stalling standard box operations. The vessel, measuring 51 meters wide with a capacity exceeding 15,000 TEU, took on the largest single shipment of yachts ever placed on a container vessel. Standard containers kept moving across adjacent bays while project teams moved heavy hulls into place.

## Parallel handling on a 366-meter hull

Moving breakbulk on container vessels demands strict space control. At Brisbane, dock workers fenced off dedicated project areas on deck to prevent foot traffic from overlapping with crane operations. Executing yacht transport logistics on an active quay required taking hulls from both land and water. The project relied on hybrid lifts quay floating setups alongside the berth. Part of the fleet arrived on low-loaders at the pier and was hoisted straight into deck cradles. The remaining yachts approached by water, positioning themselves directly under the ship's side so specialized cranes could lift them during clear tide and weather windows.

## Coordinating shore and water lifts

A container terminal in full motion operates like a massive gear train where every single tooth has a strict deadline. Inserting 15 out-of-gauge project cargo units into a tight vessel window requires advance deck engineering. Long before arrival, engineers mapped the weight, center of gravity, and windage of each yacht against ship stability limits. On deck, crews laid out custom steel beds and cradles fitted with protective mats so metal frames never touched finished paintwork. Specialized crane spreaders and padded slings were selected to match verified lifting points on each hull, preventing gelcoat scratches during tensioning.

Lifting stopped instantly whenever weather conditions degraded. During clear windows, crane crews coordinated lift times with surrounding box moves so neither team sat idle. Once landed, each hull was locked down using a combination of wedges, structural supports, chains, and welded deck fastenings. Surveyors conducted pre-load photo inspections to document the exact condition of drives, electronics, and hulls before signing off on insurance certificates and shipping documents.

## Liner schedules versus spot charters

Shippers often assume that non-containerized freight belongs strictly on multi-purpose heavy-lift ships or Ro-Ro carriers. Multi-purpose vessels handle single out-of-gauge pieces well, but their spot schedules can be irregular. Ro-Ro vessels provide consistent routes for rolling stock, yet hull height and ramp dimensions limit what they can take. Consolidating a multi-unit order on a regular liner delivers container vessel schedule reliability, fixed port calls, and lower freight bills than spot-chartered heavy-lift ships.

Parallel handling of standard boxes and breakbulk cargo works when deck sequences leave zero room for swaying. Cargo inquiries and custom shipping plans can be arranged through sales@searates.com."""

def get_tokens(text):
    return re.findall(r'\b\w+\b', text)

orig_tokens = get_tokens(orig)
draft_tokens = get_tokens(draft)

# find all maximal matching token sequences
matches = []
for i in range(len(draft_tokens)):
    for j in range(len(orig_tokens)):
        k = 0
        while i + k < len(draft_tokens) and j + k < len(orig_tokens) and draft_tokens[i+k].lower() == orig_tokens[j+k].lower():
            k += 1
        if k >= 4:
            matches.append((k, " ".join(draft_tokens[i:i+k]), " ".join(orig_tokens[j:j+k])))

# Filter sub-matches
unique_matches = []
for m in sorted(matches, key=lambda x: x[0], reverse=True):
    if not any(m[1] in u[1] and m[0] < u[0] for u in unique_matches):
        if not any(m[1] == u[1] for u in unique_matches):
            unique_matches.append(m)

for length, d_str, o_str in unique_matches:
    print(f"Length {length}: '{d_str}'")

