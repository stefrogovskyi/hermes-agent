import json
import re

source_text = """
Calculating costs and avoiding unpredictable penalties is not something you should constantly worry about. It is necessary to automate this process to carry out cargo transportation conveniently and distribute goods with maximum benefit for yourself.

By ignoring demurrage, detention, or storage charges, you will certainly miss out on costs, and they will quickly accumulate, making it difficult to forecast your logistics budget.

Using SeaRates' Demurrage & Storage Calculator, you can know your costs in advance in real time for sea containers, FTL/LTL trucking, rail freight, air freight, and even vessel downtime. Let’s explore how the tool assists you with this.

How does the tool work?
Are you a shipper planning imports/exports or a freight forwarder optimizing operations? With this tool, you get data directly from carriers around the world. Such accurate calculations help you avoid penalties and comply with requirements based on the current conditions of carriers worldwide.

The Demurrage & Storage Calculator is designed to quickly calculate and forecast costs for a single container or even an entire fleet. The functionality takes into account free days, unloading times, and carrier rates in real time. This way, you know the accurate costs and days of overrun exactly.

You can forget about searching for information directly from port or terminal operators around the world, as all the information is already collected in one place.

Manual mode:
Let’s start this overview with the familiarization of terms and disclaimer. Proceed with tooltips located at the Regime, Discharge date/Empty pick up, Gate out full, and Gate in empty/Loading date fields, as well as at the Storage, Demurrage, and Detention fields on the right side.
At this step, we have to set the baseline for when free time begins ticking:
Choose Import or export mode and dates for the Discharge/Empty pick up.
Then, input the full out gate and get the empty dates: Specify when the full container leaves the terminal ("gate out full") and when the empty one returns ("get in empty" or “loading”). These mark the end of your handling window.
- Choose the fee type — demurrage (overtime at the terminal), detention (delays outside the terminal), or storage (extended holding fees). The tool adapts calculations accordingly.
- Set free days and currency: Define the grace period provided by the carrier (e.g., 7 days for demurrage) and select your preferred currency with applicable rates.
Finalize with the Calculate button to view the total cost breakdown by each fee:
As a result, you have your own customized calculations for key fees based on live major carrier data and no longer rely on outdated tariffs.

Automatic mode:
Let’s proceed with easily filling out the form:
- Choose Import/Export in the Regime field
- Select Container Type from the drop-down list
- Enter the Port of discharge
- Find the available Shipping Line
- Specify Discharge date/Empty pick up
- Enter the Gate of Full date
- Select the Gate in Empty/Loading date
- and click on the Show tariffs button
Moving right, in the Storage section, adjust the Until day field and check the currency.
Press the Calculate button and get a full overview of storage, demurrage, and detention rates in the local currency converted to the one you have chosen before. You can change any entered data and compare results to find the most profitable option for your shipments.
Organize the storage of data by naming the result by container number or other identifiers and downloading it for further reports and analytics.
Looking for benefits details? Find a description and frequently asked questions about the Demurrage & Storage Calculator right under the tool.

White-label integration:
The demurrage and storage calculator can be a branded widget on your website.
As a logistics expert, you can fully digitize logistics by first allowing leads to accurately calculate demurrage and storage rates based on their individual needs and then book shipments with you without even leaving your website.
This white label option is a perfect fit for you as a freight forwarder, 3PL, or e-commerce provider, as your customers and users get instant penalty estimates directly on your domain.

Connect to the API:
The Demurrage & Storage Calculator API gives logistics providers and software developers automated, scalable access to penalty data that connects to your ERP or TMS. You can also create your own application based on our functionality to calculate multi-level rates and total costs in real time, set notifications, and integrate with booking systems — all for your customers’ convenience.
Our API supports all major carriers, modes of transport (sea/road/rail/air), and currencies, with authentication for high-volume operations.
Check out the API documentation, which also includes sample requests, and get your access key from the SeaRates team.
"""

article = {
  "title": "How to Use the Demurrage & Storage Calculator",
  "meta_title": "SeaRates Demurrage & Storage Calculator Guide",
  "meta_description": "Calculate demurrage, detention, and storage costs with SeaRates. Get real-time carrier tariffs, compare rates, and prevent unexpected logistics penalties.",
  "body": """Unplanned demurrage, detention, and storage fees inflate logistics budgets quickly. Late fees accumulate when free days expire unmonitored. The SeaRates Demurrage & Storage Calculator provides instant cost estimates across ocean containers, FTL and LTL trucking, rail freight, air freight, and vessel downtime.

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
}

full_text = f"{article['title']}\n{article['meta_title']}\n{article['meta_description']}\n{article['body']}"

# 1. Em-dash count
em_dash_count = sum(full_text.count(ch) for ch in ['—', '–', '--'])
print(f"Em-dash count: {em_dash_count}")

# 2. Length check
print(f"Title length: {len(article['title'])} (limit 60)")
print(f"Meta title length: {len(article['meta_title'])} (limit 60)")
print(f"Meta description length: {len(article['meta_description'])} (limit 155)")

# 3. N-gram overlap check
def normalize_text(t):
    t = re.sub(r'[^\w\s]', ' ', t.lower())
    return [w for w in t.split() if w]

src_words = normalize_text(source_text)
rew_words = normalize_text(article['body'])

def get_ngrams(words, n=6):
    return set(" ".join(words[i:i+n]) for i in range(len(words)-n+1))

src_6grams = get_ngrams(src_words, 6)
rew_6grams = get_ngrams(rew_words, 6)

overlap_6grams = rew_6grams.intersection(src_6grams)

# Filter out proper nouns / domain terms / UI field list
exemptions = [
    "regime discharge date empty pick up",
    "discharge date empty pick up gate",
    "gate out full gate in empty",
    "ltl trucking rail freight air freight",
    "trucking rail freight air freight and",
    "sea road rail and air modes"
]

non_exempt_overlaps = []
for og in overlap_6grams:
    if not any(ex in og for ex in exemptions):
        non_exempt_overlaps.append(og)

print(f"Total 6-gram overlaps: {len(overlap_6grams)}")
print(f"Non-exempt 6-gram overlaps: {len(non_exempt_overlaps)}")
for og in non_exempt_overlaps:
    print(f"  Overlap: '{og}'")

# 4. Contrastive negation check
instead_of_count = article['body'].lower().count("instead of")
not_count = len(re.findall(r'\bnot\b', article['body'].lower()))
print(f"'instead of' count: {instead_of_count}")
print(f"'not' count: {not_count}")

with open('/opt/hermes/profiles/archie/verified_article.json', 'w', encoding='utf-8') as f:
    json.dump(article, f, ensure_ascii=False, indent=2)
