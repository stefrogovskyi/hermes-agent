---
name: local-business-leadgen
description: "Use when finding businesses without websites on Google Maps."
version: 1.0.0
author: Ben Jett (Avalanche Agency)
license: MIT
metadata:
  hermes:
    tags: [LeadGen, Google Maps, Outreach, Sales, BANT, CRM, Local Business]
---

# Local Business Lead Generation & Outreach Pipeline

## When to Use
Use when identifying local SMBs on Google Maps / OSM lacking websites, generating cold B2B outreach pitches, and managing lead pipelines in Google Sheets CRM.

## References
- `references/whatsapp_gateway_setup.md` — Setup, persistence, rate-limiting, and dispatch flow for local Baileys WhatsApp Web multi-device gateway.
- `references/cold_email_smtp_imap.md` — SMTP RFC standards, MailChannels anti-spam bypass, `INBOX.Sent` IMAP sync, and HTML signature templates.
- `references/outscraper_rapidapi_fallback.md` — Resilient failover architecture between RapidAPI and Outscraper, schema normalization, and Google Sheets `#ERROR!` formula escaping.

## Architecture

1. **Targeting & Geography:** Focus on high-ticket service verticals (Auto Detailing, Dental/Cosmetics, Roofing, HVAC, Legal) in metropolitan areas.
2. **Dual Extraction Strategy:**
   - **Plan B (Fast API / Outscraper / RapidAPI Google Places):** Query by category + city, filter by `websiteUri IS NULL` or broken URL, extract verified phone number and Google rating (4.5★+ with active reviews).
   - **Plan A (Fallback Open-Source / OSM Bbox):** Overpass API / Nominatim bounding box query without website tags.
3. **Qualification & Value Hook:**
   - Detect absence of direct mobile booking and 24/7 client intake.
   - Generate personalized BANT pitch with reference to their Google Maps rating and local area.
4. **CRM Sync (Google Sheets):**
   - Populate Google Sheets CRM (`Leads Pipeline`, `Outreach Scripts`, `Niche Strategy`).
   - Track delivery channels (SMS, WhatsApp, Direct Call, Email).
   - Store lead metadata: ID, date, niche, city, company, phone, rating, reviews count, address, pitch, status, deal size.
5. **Outreach & Communications Integration:**
   - **1-Click Direct Outreach Links (Google Sheets):** Embed `=HYPERLINK("https://wa.me/<phone>?text=<encoded_msg>", "💬 Send WhatsApp")` and `=HYPERLINK("tel:+<phone>", "📞 Call Now")` for immediate no-code dispatch.
   - **Twilio SMS / WhatsApp API:** Connect using `Account SID`, `Auth Token` or `API Key/Secret`, and registered Twilio phone number.
   - **Branded Email Inbound:** Automated forwarding from domain address (`contact@domain.com` -> inbox).
   - **Automated Scheduling:** Daily batch ingestion via cron tasks.

## Key Operating Directives
- **Hard KPI Goal: 20 Delivered Contacts Daily:** The pipeline does not merely scrape 20 rows; it actively loops through multi-city and multi-niche query pools until exactly 20 contacts receive a delivered WhatsApp message or Email.
- **Universal Google Rating Spectrum & Reputation Angle:** Businesses of any rating are targeted. For ratings < 4.0, pitch pivots to an automated reputation recovery & private feedback routing angle alongside 24/7 AI booking.
- **Schedule & Delays:** Cron runs daily at 19:00 Kyiv (16:00 UTC). Delay between successful sends is 120-150s (2-2.5 min) to complete within the 3600s cron timeout ceiling while maintaining anti-spam protection.
- **Signature & Link:** Ben Jett, Account Executive, Avalanche Agency, linking directly to https://aavalanche.com.
- **Anti-Spam Dynamic Pitch Variations:** Greetings, hooks, pain points, value propositions, and CTAs are dynamically shuffled per lead to prevent pattern detection.
- **Enrichment Module:** Public registries and business directories are scanned for emails to run multichannel outreach.
- **Anti-Spam Dynamic Text Variations (Crucial):** Never dispatch identical boilerplate templates to multiple leads. Construct modular variation engines (4 greetings × 4 niche hooks × 4 pain points × 4 value props × 4 CTAs) to generate uniquely phrased messages for every lead. Enforce a minimum length check (>50 chars) and guard against placeholder strings before transmission.
- **Root Domain Links:** For outreach footers and signatures, use clean top-level domain URLs (`https://aavalanche.com`) rather than subpages unless specifically requested.
- **Cold Email IMAP Sent Sync & Anti-Spam (MailChannels):** SMTP transmission does not automatically copy messages to webmail `Sent` folders. Append sent messages via IMAP directly to `INBOX.Sent` with the `\Seen` flag. Ensure valid `Message-ID`, RFC `Date`, `From`, `Reply-To`, `X-Mailer`, and dual `text/plain` + `text/html` multipart payloads to prevent `550 5.7.1 [CS]` MailChannels/Hostinger blocks.
- **Google Sheets API Rate Limits:** Always use single-range updates (`values().update()`) or batch updates across entire columns rather than making single-cell API calls inside loops, preventing HTTP 429 quota exhaustion.
- **Twilio A2P 10DLC Compliance:** Purchasing US phone numbers for SMS requires A2P 10DLC registration. For instant zero-setup outreach, use 1-Click `wa.me` links or web-based WhatsApp bridges.
- **WhatsApp Phone Numbers:** Official Meta/Twilio WhatsApp Business requires an unlinked number. Do not use an active personal WhatsApp number directly with Twilio API without disconnecting it first.
- **RapidAPI Subscription State:** RapidAPI endpoints require active subscription to the specific API tier (even free tier) before keys become valid (otherwise returns 403/429).
- **Google Sheets Formatting & Tab Names:** When batch updating/styling via Sheets API, ensure sheet tab IDs and names are queried dynamically rather than assuming `sheetId: 0` or default `'Sheet1'` (e.g. use exact tab name `"'Leads Pipeline'!A:O"` with single quotes around multi-word titles to avoid HTTP 400 "Unable to parse range").
- **Google Sheets `+` Phone Number Formula Parse Bug (`#ERROR!`):** In Google Sheets, any cell string that begins with a plus sign (e.g. `+1 720-999-6857`) is automatically evaluated by Sheets as an arithmetic addition formula. When the string contains dashes, parentheses, or phone characters, Google Sheets errors out with `#ERROR!` (Formula parse error). To prevent this, always prepend an apostrophe to the phone string (e.g. `phone_val = f"'{phone}" if phone and str(phone).startswith('+') else (phone or "N/A")`) before appending rows to the CRM, guaranteeing that international phone numbers render cleanly as formatted text.
- **API Quota Exhaustion & Automatic Outscraper Fallback:** Free/basic tiers of RapidAPI Google Places enforce daily request ceilings (`HTTP Error 429: Too Many Requests`). When 429 occurs, scripts must not fail or abort mid-run. Implement an automatic in-memory fallback to Outscraper Maps Search API (`https://api.app.outscraper.com/maps/search-v3?query={query}&limit=20&async=false` with header `X-API-KEY: <key>`), normalizing Outscraper fields (`name`, `phone`, `site`/`website`, `rating`, `reviews`, `full_address`) into standard Places schema so the outreach loop seamlessly fulfills the 20/20 daily contact KPI.
