import json
import re

title = "How to Use the Demurrage & Storage Calculator"
meta_title = "SeaRates Demurrage & Storage Calculator Guide"
meta_description = "Calculate demurrage, detention, and storage costs with SeaRates. Get real-time carrier tariffs, compare rates, and prevent unexpected logistics penalties."

body = """Unplanned demurrage, detention, and storage fees inflate logistics budgets quickly. Late fees accumulate when free days expire unmonitored. The SeaRates Demurrage & Storage Calculator provides instant cost estimates across ocean containers, FTL and LTL trucking, rail freight, air freight, and vessel downtime.

### Live Carrier Tariffs

Instead of contacting port or terminal operators individually, shippers and freight forwarders access live carrier data in one place. Using real-time rate lookup & penalty forecasting gives teams early visibility before fees accrue.

### Manual Mode Setup

Review terms, disclaimers, and tooltips across Regime, Discharge date/Empty pick up, Gate out full, Gate in empty/Loading date, Storage, Demurrage, and Detention.

Select Import or Export in the Regime field, then enter dates for discharge or empty pickup. Enter gate out full to log container departure from the facility. Specify gate in empty or loading to set when the empty container returns. These inputs define the handling window.

Proper terminal storage surcharges & detention rate management requires choosing the right fee category:
- Demurrage applies to overtime at the terminal.
- Detention covers delays outside the terminal.
- Storage applies to extended holding fees.

Set carrier free days and pick a preferred currency. Click Calculate to view total cost breakdowns based on live major carrier tariffs.

### Automatic Mode Calculations

Automatic mode simplifies entries through drop-down menus.

Select Import or Export, pick a container type, specify the discharge port, and choose an available shipping line. Input discharge or empty pickup dates alongside gate out full and gate in empty or loading dates, then click Show tariffs.

In the Storage section, set the target end date and review the active currency. Click Calculate to view storage, demurrage, and detention rates converted into chosen local currency. Modifying parameters lets users compare options. Results can be named by container number or custom identifiers and downloaded for reports and analytics.

The tool calculates overrun days based on free time rules. FAQs and detailed benefit descriptions sit directly beneath the calculator.

### Integration Options

Freight forwarders, 3PLs, and e-commerce providers can add a white-label container cost estimator widget to their domain, allowing clients to calculate penalties and book shipments directly.

Software teams can implement TMS/ERP API integration to connect penalty data into internal systems. The API supports multi-level rate calculations, real-time total costs, automated notifications, and booking system connections. It covers major carriers, sea, road, rail, and air modes, alongside multi-currency support and high-volume authentication. Developers can access API documentation and sample requests, then request an access key from SeaRates."""

# Checks
print(f"Title len: {len(title)} (<= 60)")
print(f"Meta Title len: {len(meta_title)} (<= 60)")
print(f"Meta Desc len: {len(meta_description)} (<= 155)")

# Check em dash, double hyphen, en dash
dashes = [d for d in ["—", "--", "–"] if d in title + meta_title + meta_description + body]
print(f"Dashes found: {dashes}")

# Contrastive negations
cn_matches = re.findall(r'\brather than\b|\binstead of\b|,\s*not\b', body, re.IGNORECASE)
print(f"Contrastive negations found ({len(cn_matches)}): {cn_matches}")

# Check specific overlaps and fixes
print("\n--- Overlap 1 Check ---")
print("Old overlap present?", "when the full container leaves the terminal" in body)

print("\n--- Overlap 2 Check ---")
print("Old overlap present?", "the Storage section, adjust the Until day field and check" in body)

print("\n--- Issue 1 Check ---")
print("container tracking present?", "container tracking" in body)

print("\n--- Issue 2 Check ---")
print("automated free time tracking present?", "automated free time tracking" in body)

print("\n--- Issue 3 Check ---")
print("drayage present?", "drayage" in body)

print("\n--- Issue 4 Check ---")
print("ocean freight restriction present?", "API integration for ocean freight" in body)

data = {
    "title": title,
    "meta_title": meta_title,
    "meta_description": meta_description,
    "body": body
}

with open("/opt/hermes/profiles/archie/test_out.json", "w") as f:
    json.dump(data, f, indent=2)

print("\nSaved output to test_out.json")
