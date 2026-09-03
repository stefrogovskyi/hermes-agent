import json

candidate = {
  "title": "Instagram Growth Strategy for Small Freight Forwarders",
  "meta_title": "Instagram Marketing Guide for Small Shipping Companies",
  "meta_description": "Build freight forwarding engagement on Instagram. Use short-form video Reels, 24-hour Stories, and shipment visibility tools to reach target accounts.",
  "body_text": """Industry giants control massive ocean fleets, yet authentic human presence remains a currency automated systems cannot manufacture. Enterprise carriers post stock imagery of warehouse workers. Their comment responses feel like rigid corporate scripts. Independent operators show real facility tours, fleet maintenance procedures, and package delivery workflows. Show real work. Executing humanized B2B branding through real warehouse operations builds credibility among prospective clients. Content calendars keep posting consistent. Overly complex schedules must not replace genuine communication.

## 24-Hour Updates and Audience Interactions

Instagram Stories disappear after 24 hours. They show raw day-to-day operations that do not belong on a permanent profile grid. Forwarders publish quick updates from port terminals or driver loading bays.

Interactive polls and question stickers gather feedback on service routes. Limited-time discount codes convert viewers into immediate quote requests. Flash sales running for 24 hours create urgency for open container space.

Increased Story views improve account ranking. The platform distributes future posts to broader audiences as view duration increases. Expanded visibility strengthens client relationships across active shipping lanes.

## Video Content Creation

Reels deliver video content through short clips. Strong opening frames, clear audio, and simple narrative structures attract viewer attention. AI video generators help small teams convert fleet logs, client testimonials, and behind-the-scenes logistics footage into short-form video Reels without extra video production staff.

Trending audio tracks, industry humor, and hashtags like #logisticslife expand organic algorithmic reach among younger logistics coordinators.

## Bio Configuration and Account Engagement

A profile bio introduces core transport services and links to shipment visibility tools for active cargo tracking. Story Highlights organize essential company information into categories for routes, field staff, and verified client references. Observing competitor profiles helps identify standard layout patterns before publishing a custom bio.

Direct message management drives freight forwarding engagement across active social channels. Teams must reply manually to incoming inquiry messages and public comment questions. Automated response scripts alienate prospects. Replying directly to operational questions, offering quick freight consultations, and addressing service complaints professionally converts public inquiries into active accounts.

## Paid Boosts and Analytics Tracking

Organic post distribution faces platform limitations. Combining organic updates with targeted Instagram Ads balances reach. Paid boosts generate likes on top-performing posts, sending positive signals to the distribution algorithm. Promoted posts appear in recommendation feeds and local geographical search results.

Weekly analytics reviews reveal performance metrics. Account dashboards show top-performing posts, audience location demographics, and active viewing hours. Adjusting posting schedules, hook text, and graphic colors based on weekly data improves content performance. Business expansion may require hiring dedicated social media personnel to manage ongoing campaigns."""
}

with open("candidate.json", "w", encoding="utf-8") as f:
    json.dump(candidate, f, indent=2)

print("candidate.json written successfully.")
