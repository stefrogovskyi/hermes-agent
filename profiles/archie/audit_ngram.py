import re

source = """The importance of safety signs in the workplace cannot be overstated. While some workplaces are more hazardous than others, there are hazards in all work environments, whether this is a construction site, industrial zone, laboratory, or standard office. This means that safety must be paramount in all work environments, and one of the best ways to enhance safety is with the use of safety signs. Safety signs can communicate important messages to workers, customers, and other visitors to pre-vent accidents from occurring. Choosing the right safety signs is key, so this post will show you how to go about choosing the right signs for any hazardous area.
Identifying The Hazards
First, you need to identify the hazards in your workplace (in a port, warehouse, transshipment point, etc.). A risk assessment will help you identify the risks, which will then make it much easier to choose the right sign. The main types of hazards include:
Environmental
Chemical
Biological
Electrical
Mechanical
Choosing The Right Sign Category
Within each category of hazard, there are standardized colors and symbols used that align with international safety regulations to make logistics operations safety as any other industry so far. This is important because it means that these signs are instantly recognizable and understandable to all workers and visitors. The color meanings include:
Yellow/Amber: Warning signs to take care
Red: Prohibitory signs
Green: Indicates the location of fire exits, evacuation routes, and other important sites
Blue: Mandatory signs indicating an action that must be taken
If selecting appropriate radiation hazard signs, for example, then you will need to choose a hazardous substances sign, which will feature a hazard warning triangle with the color yellow. This is why you must always obtain your hazard signs from a recognized and established safety sign supplier.
Material
In addition to choosing the right safety sign category, you must also consider the material the sign is made from. You should consider where the sign will be placed and if there are any potential factors that could damage the sign, such as weather, chemicals, or temperatures. Be sure to choose a sign that will be able to withstand the environment, such as signs with UV-resistant coatings, if the sign will be exposed to constant and/or high levels of UV.
Placement
Placement is another key consideration when it comes to safety signs. You need to communicate the safety information at the right time, so you need to place the sign somewhere that it will be visible before the hazard becomes a danger to the worker/visitor. Crucially, it must also be somewhere that is highly visible. This means placing the sign at eye level in a well-lit area (you can also get glow-in-the-dark or illuminated signs for low-light areas).
The information in this post should be useful when it comes to selecting workplace safety signs for hazardous areas. Logistics workplace may have hazards, some more than others, and safety signs are critical for communicating important safety information to workers, customers, and any other visitors you have. By identifying the hazards, choosing the right sign category, selecting an appropriate material, and placing the sign strategically, you can reduce risk and create a safer environment for all."""

rewrite = """Selecting Safety Signs for Port and Warehouse Areas

A port terminal or busy warehouse moves hundreds of tons of freight every hour, leaving little room for miscommunication when a hazard appears. Risk exists in every workplace, from busy transshipment hubs to quiet administrative offices, making physical safety signage a simple direct line of defense for staff, drivers, and visitors.

### Mapping Site Risks Across Operations

Effective sign selection starts with systematic port and warehouse hazard identification. Safety managers evaluate working areas through structured risk assessments to categorize potential exposure across five standard operational threat types:
* Environmental risks caused by climate or site conditions.
* Chemical hazards from stored or transported substances.
* Biological risks in specialized storage or waste handling.
* Electrical risks around high-voltage equipment and power feeds.
* Mechanical threats near heavy machinery and conveyors.

Recognizing these specific exposures narrows down the required signage for each zone.

### Standardized Categories and Color Coding

International safety regulations rely on ISO 7010 safety signs so workers instantly understand warnings across global supply chains. Sourcing signs from established, recognized suppliers ensures symbols match standardized categories and universal color codes:
* Yellow or Amber: Warning signs indicating caution. Hazardous substance markers, such as a radiation warning triangle, use a yellow background.
* Red: Prohibitory signs banning specific actions or entry.
* Green: Emergency guidance designating fire exits, evacuation routes, and first aid points.
* Blue: Mandatory signs directing required actions, such as wearing personal protective equipment.

Matching the hazard to the exact category keeps facilities compliant and avoids confusion during routine work or emergency responses.

### Matching Materials and Placement to Working Conditions

Choosing the proper sign classification is only half the task. Physical durability and precise safety signage placement determine whether a sign remains readable over time.

Outdoor yards, dockside terminals, and chemical storage areas demand durable physical builds. Substantial sunlight degrades standard plastics, so outdoor areas require UV-resistant sign materials with protective coatings. Exposure to extreme temperatures, heavy weather, or airborne chemicals must also guide material selection.

Positioning requires equal attention. A sign must be visible before someone enters a danger zone, giving them time to react safely. Mount signs at eye level in brightly lit spots. For dimly lit aisles or night operations, photoluminescent or internally illuminated signs maintain visibility when ambient lighting drops.

Systematic hazard assessment, compliant color matching, resistant materials, and strategic mounting combine to maintain hazardous area compliance across all terminal and facility operations."""

def get_words(text):
    return re.findall(r'\b\w+\b', text.lower())

src_words = get_words(source)
rew_words = get_words(rewrite)

n = 6
src_ngrams = set(tuple(src_words[i:i+n]) for i in range(len(src_words)-n+1))
rew_ngrams = [tuple(rew_words[i:i+n]) for i in range(len(rew_words)-n+1)]

overlaps = [gram for gram in rew_ngrams if gram in src_ngrams]

print(f"Total 6-gram overlaps count: {len(overlaps)}")
for o in set(overlaps):
    print("Overlap:", " ".join(o))

