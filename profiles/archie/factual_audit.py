import sys

# Let's write out every claim in the rewrite and map it to the original text.

claims = [
    {
        "location": "Title",
        "rewrite_claim": "SeaRates Headed to VDS 2024 in Valencia",
        "original_ref": "Title: SeaRates Х VDS 2024: Upcoming Conference Announcement ... attending VDS, which will take place October 23-24 in Valencia, Spain.",
        "status": "ACCURATE"
    },
    {
        "location": "Meta Title & Description",
        "rewrite_claim": "SeaRates at VDS 2024 in Valencia: Connect With Our Team / Meet SeaRates and Olexandr Grabarchuk at VDS 2024 in Valencia on Oct 23-24 to discuss shipping and logistics solutions. Contact sales@searates.com.",
        "original_ref": "Meet our main representative at VDS 2024: Olexandr Grabarchuk ... emailing us at sales@searates.com.",
        "status": "ACCURATE"
    },
    {
        "location": "Body - Paragraph 1",
        "rewrite_claim": "The SeaRates team is attending VDS 2024 on October 23-24, hosted at the City of Arts and Sciences in Valencia, Spain.",
        "original_ref": "SeaRates team will be attending VDS, which will take place October 23-24 in Valencia, Spain... VDS will be held in Valencia, Spain, at the City of Arts and Sciences on October 23-24.",
        "status": "ACCURATE"
    },
    {
        "location": "Body - Paragraph 1",
        "rewrite_claim": "The gathering brings together representatives from international startups, global corporations, and institutional investors.",
        "original_ref": "...surrounded by representatives of high-profile global startups and corporations that encourage numerous investors at VDS events.",
        "status": "MINOR EXTRAPOLATION / SLIGHT CHANGE ('institutional investors' vs 'numerous investors')"
    },
    {
        "location": "Body - Paragraph 1",
        "rewrite_claim": "Centered on this year's theme, 'Embracing Evolution: Invest in the Leaders of Tomorrow', discussions will focus on how modern technological advancements shape logistics, trade, and broader industry sectors.",
        "original_ref": "explore this year's theme 'Embracing Evolution: Invest in the Leaders of Tomorrow' and dive deeper into the positive aspects of the development of industries and society due to the modern technological revolution.",
        "status": "ACCURATE"
    },
    {
        "location": "Body - Paragraph 2 (H2)",
        "rewrite_claim": "## Industry Leaders Gather in Valencia",
        "original_ref": "N/A - Heading added by rewrite.",
        "status": "ADDED STRUCTURE"
    },
    {
        "location": "Body - Paragraph 3",
        "rewrite_claim": "VDS 2024 expects 12,000+ attendees, 600+ speakers, 700+ investors, and 2,500+ startups from across the world.",
        "original_ref": "Over 12,000 attendees, 600+ speakers, 700+ investors, and 2,500+ start-ups from different global industries gathered...",
        "status": "ACCURATE"
    },
    {
        "location": "Body - Paragraph 3",
        "rewrite_claim": "Presentations and discussions will span eight dedicated spaces across the venue: the Main, Santander, Green, Audiovisual, Discovery, and Pitch Stages, alongside the Workshop Room & VIP Boxes.",
        "original_ref": "...listen to in the Main, Santander, Green, Audiovisual, Discovery, and Pitch Stages, as well as in the Workshop Room & VIP Boxes in line with the VDS agenda.",
        "status": "INVENTED / EXTRAPOLATED DETAILS: Original lists 6 stages ('Main, Santander, Green, Audiovisual, Discovery, and Pitch Stages') + 'Workshop Room & VIP Boxes'. Rewrite synthesizes/counts this into 'span eight dedicated spaces across the venue' (counting Workshop Room as 1 and VIP Boxes as 1 to reach 8, or counting 6 stages + Workshop Room + VIP Boxes = 8). Original does NOT specify the count 'eight dedicated spaces'."
    },
    {
        "location": "Bullet 1",
        "rewrite_claim": "Practical AI adoption for global businesses, sustainable investment strategies, and resilient supply chain formation",
        "original_ref": "Revolutionary AI technologies for businesses around the world: ways to successfully collaborate, transform, strengthen, improve, empower sectors, sustainable technology and investment strategies, and supply chain formation",
        "status": "EXTRAPOLATION / INVENTED ATTRIBUTES: Original says 'Revolutionary AI technologies', rewrite changes to 'Practical AI adoption'. Original says 'supply chain formation', rewrite invents 'resilient supply chain formation'."
    },
    {
        "location": "Bullet 2",
        "rewrite_claim": "Startup ecosystem growth, pitch competitions, and presentation sessions",
        "original_ref": "All about startups: building ecosystems, presentation sessions, competitions, etc.",
        "status": "ACCURATE PARAPHRASE"
    },
    {
        "location": "Bullet 3",
        "rewrite_claim": "Joint innovation initiatives linking tech developers with port operations",
        "original_ref": "Opportunities for joint development for the innovation community and the port industry",
        "status": "EXTRAPOLATION: 'innovation community' changed to 'tech developers', 'port industry' changed to 'port operations'."
    },
    {
        "location": "Bullet 4",
        "rewrite_claim": "Regional investment analysis highlighting opportunities across South America and Europe",
        "original_ref": "Overview of the investment landscape in global regions, such as South America and Europe",
        "status": "EXTRAPOLATION: Original says 'Overview of the investment landscape', rewrite says 'Regional investment analysis highlighting opportunities'."
    },
    {
        "location": "Bullet 5",
        "rewrite_claim": "Collaborative funding frameworks between maritime entrepreneurs and public agencies",
        "original_ref": "Opportunities for cooperation between public funding bodies and maritime entrepreneurship",
        "status": "ACCURATE PARAPHRASE ('public funding bodies' -> 'public agencies', 'cooperation' -> 'collaborative funding frameworks')"
    },
    {
        "location": "Bullet 6",
        "rewrite_claim": "Scalable financial technologies tailored for international commerce",
        "original_ref": "Scaling of financial technologies",
        "status": "INVENTED / EXTRAPOLATED DETAIL: Original only says 'Scaling of financial technologies'. Rewrite extrapolates 'tailored for international commerce'."
    },
    {
        "location": "Bullet 7",
        "rewrite_claim": "Emerging workplace trends, including social transformation and business mental health initiatives",
        "original_ref": "Trends and aspects of social transformation and overcoming mental health challenges in business",
        "status": "EXTRAPOLATION: Original says 'social transformation and overcoming mental health challenges in business', rewrite adds 'Emerging workplace trends' and 'business mental health initiatives'."
    },
    {
        "location": "Schedule Sentence",
        "rewrite_claim": "Detailed schedule information for both days is available on the official VDS website. Attendees can review session times and speaker lineups prior to arriving in Valencia.",
        "original_ref": "For more information about the agenda on the first and second days, visit the VDS website.",
        "status": "INVENTED / FABRICATED CLAIM: Original only says to visit the VDS website for agenda info. Rewrite invents: 'Attendees can review session times and speaker lineups prior to arriving in Valencia.'"
    },
    {
        "location": "Meet Olexandr Section",
        "rewrite_claim": "Olexandr Grabarchuk will represent SeaRates on site throughout the two-day event. Our team is available to meet with clients, partners, and industry peers to exchange insights on freight movement and digital trade tools. Whether you want to streamline cargo operations or evaluate digital tools for your freight requirements, we welcome the opportunity to connect in person.",
        "original_ref": "Meet our main representative at VDS 2024: Olexandr Grabarchuk ... Find the SeaRates team live and come talk to us about how we can help you with your business needs and enhance the digital aspect of your logistics and trading. We would be delighted to discuss with you how we might assist you with your shipping requirements.",
        "status": "ACCURATE / PARAPHRASED"
    },
    {
        "location": "CTA / Email Section",
        "rewrite_claim": "To arrange a dedicated meeting with our team during VDS 2024 or learn more about our upcoming event appearances, send an email to sales@searates.com. We look forward to meeting you in Valencia this October.",
        "original_ref": "Get more information about forthcoming conferences and learn more about SeaRates by emailing us at sales@searates.com. We hope to see you in Valencia in October!",
        "status": "EXTRAPOLATION / FABRICATED PURPOSE: Original says email sales@searates.com to 'Get more information about forthcoming conferences and learn more about SeaRates'. Rewrite adds 'To arrange a dedicated meeting with our team during VDS 2024 or learn more about our upcoming event appearances'."
    }
]

print("=== FACTUAL INTEGRITY AUDIT SUMMARY ===")
for c in claims:
    print(f"[{c['location']}] - {c['status']}")
    print(f"   Rewrite : {c['rewrite_claim']}")
    print(f"   Original: {c['original_ref']}\n")

