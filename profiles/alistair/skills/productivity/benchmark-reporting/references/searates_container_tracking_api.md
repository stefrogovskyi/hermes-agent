# SeaRates Container Tracking API v3.0 Reference

## Base Endpoint
```
https://tracking.searates.com/tracking
```

## Authentication & Parameters
- SeaRates uses query-string authentication: `?api_key=YOUR_API_KEY`.
- **Query Parameters:**
  - `api_key` *(string, required)*: Customer API key.
  - `number` *(string, required)*: Container number (e.g. `MSKU7117653`), Bill of Lading (B/L), or Booking number.
  - `sealine` *(string, optional)*: Carrier SCAC code (e.g. `MSCU`, `MAEU`, `HLCU`, `CMDU`, `COSU`, `ONEY`).
  - `type` *(string, optional)*: Document type (`CT` for Container Tracking, `BL` for Bill of Lading, `BK` for Booking).

## Request Examples
### cURL
```bash
curl -s "https://tracking.searates.com/tracking?api_key=K-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX&number=MSKU7117653"
```

### Python
```python
import urllib.request, urllib.parse, json

api_key = "K-XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
number = "MSKU7117653"
url = f"https://tracking.searates.com/tracking?api_key={api_key}&number={number}"

req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read().decode("utf-8"))
```

## Response Statuses & Error Codes
| Message | Status | Description / Root Cause |
|---|---|---|
| `OK` | `success` | Request completed successfully. Container/B/L events and route returned. |
| `SEALINE_HASNT_PROVIDE_INFO` | `success` | Carrier replied that nothing was found for this request. |
| `NO_CONTAINERS` | `success` | Line returned shipment metadata but no container units. |
| `NO_EVENTS` | `success` | Container exists but carrier has recorded no milestone events yet. |
| `WRONG_PARAMETERS` | `error` | Missing required parameters (e.g. missing `api_key` or `number`). |
| `WRONG_NUMBER` | `error` | Invalid B/L or booking number format / check digit. |
| `WRONG_SEALINE` | `error` | Invalid carrier alpha code (SCAC) specified. |
| `WRONG_TYPE` | `error` | Specified document type is invalid (must be `CT`, `BL`, or `BK`). |
| `API_KEY_WRONG` | `error` | Invalid API key, unactivated key, or key revoked on SeaRates billing. |
| `API_KEY_ACCESS_DENIED` | `error` | API key lacks permission for the Container Tracking product. |
| `API_KEY_EXPIRED` | `error` | API key subscription period has expired. |
| `API_KEY_LIMIT_REACHED` | `error` | API key quota exhausted (out of lookups/credits). |
| `API_KEY_RATE_LIMIT` | `error` | Request rate limit exceeded. |
