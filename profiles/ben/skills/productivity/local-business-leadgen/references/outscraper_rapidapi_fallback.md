# Outscraper & RapidAPI Google Maps Lead Extraction & Resilient Failover

## Overview
When extracting local business leads without websites, relying on a single API provider risks pipeline interruption due to rate limits (`HTTP 429: Too Many Requests`) or daily quota exhaustion. This reference specifies the exact implementation for continuous, autonomous multi-source lead scraping and CRM normalization.

## RapidAPI Google Places Endpoint (Primary)
- **Host:** `google-map-places-new-v2.p.rapidapi.com`
- **Path:** `/v1/places:searchText`
- **Method:** `POST`
- **Headers:**
  - `Content-Type`: `application/json`
  - `X-Goog-FieldMask`: `places.id,places.displayName,places.formattedAddress,places.nationalPhoneNumber,places.rating,places.userRatingCount,places.websiteUri`
  - `x-rapidapi-host`: `google-map-places-new-v2.p.rapidapi.com`
  - `x-rapidapi-key`: `<RAPIDAPI_KEY>`
- **Payload:**
  ```json
  {
    "textQuery": "emergency plumber in Chicago IL",
    "maxResultCount": 20
  }
  ```

## Outscraper Maps Search-v3 (Automatic Fallback)
- **Endpoint:** `https://api.app.outscraper.com/maps/search-v3`
- **Method:** `GET`
- **Query Params:** `query=<url_encoded_query>&limit=20&async=false`
- **Headers:** `X-API-KEY: <OUTSCRAPER_API_KEY>`
- **Response Normalization:**
  Outscraper returns a nested list `data[0]`. Map each element to standard Places schema:
  ```python
  def normalize_outscraper_place(item):
      site = item.get('site') or item.get('website') or ""
      return {
          'id': item.get('place_id') or item.get('google_id') or str(uuid.uuid4()),
          'displayName': {'text': item.get('name', '')},
          'formattedAddress': item.get('full_address') or item.get('address') or f"{item.get('city', '')}, {item.get('state', '')}",
          'nationalPhoneNumber': item.get('phone', ''),
          'rating': item.get('rating', 0),
          'userRatingCount': item.get('reviews', 0),
          'websiteUri': site if site and site.lower() != 'none' else None
      }
  ```

## Google Sheets CRM Data Integrity
1. **Leading Plus Bug (`#ERROR!`):**
   - Google Sheets parses any cell beginning with `+` as an arithmetic formula.
   - For all international phone numbers, always prepend an apostrophe:
     ```python
     phone_val = f"'{phone}" if phone and str(phone).startswith('+') else (phone or "N/A")
     ```
2. **Sheet Tab Escaping:**
   - Always enclose sheet titles with spaces in single quotes when passing ranges to Google Sheets API:
     ```python
     range_spec = "'Leads Pipeline'!A:O"
     ```
