---
name: b2b-pricing-calculator
description: "Evaluate B2B client pricing, volume tiers, and proposals."
version: 0.1.0
author: Richard Marlowe, Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Pricing, B2B, Sales, Calculator, Negotiation, Navo24]
---

# B2B Sales Pricing Calculator & Deal Evaluation Playbook

This skill defines the evaluation methodology and negotiation logic used by Richard Marlowe (Senior B2B Sales Manager & Mentor) when sales representatives (Nikita, Liliia, Alona, Oleg, Kate) consult on deal pricing.

## When to Use

- When a sales manager asks how much to quote a prospective client.
- When structuring B2B proposals for TrackingMCP (Ocean & Air), Schedules, or Rates.
- When negotiating between Pay-As-You-Go (PAYG) and Annual Prepayment plans.
- When qualifying deal size, volume discounts, and floor margins.

---

## 🧭 Step 1: Mandatory Clarifying Questions (Discovery Gate)

**RULE: NEVER quote a blind price without qualifying the prospect.**
When a sales manager asks "How much should I charge Company X?", ALWAYS ask the following 5 clarifying questions first:

1. 🌍 **Country & HQ Location:** In which country is the client registered / operating? (G20/Tier 1 vs. Developing/Tier 3).
2. 👥 **Company Size & Revenue:** Approximately how many employees do they have, or what is their estimated annual turnover? (<50 staff, 100–500, or 1000+ Enterprise / >$10M).
3. 📦 **Expected Shipment Volume:** How many unique shipments (containers/BLs) do they handle per month or per year?
4. 🔥 **Client Appetite & Urgency:** 
   - What is driving the request? (Migrating from SeaRates/project44/Vizion, building a new customer portal, formal tender?).
   - Are they budget-sensitive or is data quality/speed their top priority?
5. 💳 **Preferred Billing Model:** Do they prefer monthly Pay-As-You-Go (post-paid) or are they open to an Annual Prepayment plan with a 25% discount?

---

## 📐 Step 2: Core Pricing Formula & Limits (TrackingMCP)

### Price Ceilings & Floors per Unique Shipment
| Billing Model | Base Ceiling Rate | Absolute Floor Rate | Billing Terms |
| :--- | :--- | :--- | :--- |
| **Pay-As-You-Go (PAYG)** | **$4.00** / shipment | **$0.60** / shipment | Monthly in arrears (Net 14) |
| **Annual Prepay (Year Ahead)** | **$3.00** / shipment | **$0.45** / shipment | 100% upfront (25% built-in discount) |

### Base Volume Curve (Price per Unique Shipment)
- **Micro Volume (1 – 30 shipments/mo):** **$4.00 PAYG / $3.00 Annual** *(Or Starter Plan: $50/mo up to 25 shipments)*.
- **Low Volume (31 – 100 shipments/mo):** **$3.20 PAYG / $2.40 Annual**.
- **Mid Volume (101 – 300 shipments/mo):** **$2.40 PAYG / $1.80 Annual**.
- **Growing Volume (301 – 750 shipments/mo):** **$1.80 PAYG / $1.35 Annual**.
- **High Volume (751 – 2,000 shipments/mo):** **$1.20 PAYG / $0.90 Annual**.
- **Enterprise Volume (2,001 – 5,000 shipments/mo):** **$0.85 PAYG / $0.65 Annual**.
- **Mega / Platform Volume (>5,000 shipments/mo):** **$0.60 PAYG / $0.45 Annual** *(Absolute Floor)*.

### Modifiers (Geo, Size, Appetite)
- **Geography:**
  * **G20 / Tier 1 (US, UK, DE, FR, NL, SG, AE, AU, CA, JP):** `+15%` premium (high ability to pay).
  * **Tier 2 (Eastern Europe, Turkey, LATAM, South Africa):** `0%` baseline.
  * **Tier 3 / Developing (India, Pakistan, Bangladesh, Egypt, Nigeria, Vietnam, Indonesia):** `-20%` adjustment.
- **Company Size:**
  * **Enterprise (>1,000 employees OR >$10M revenue):** `+15%`.
  * **Mid-market (50–1,000 employees):** `0%`.
  * **Small / Micro (<50 employees AND <$1M revenue):** `-15%`.
- **Client Appetite:**
  * **High Urgency / Quality-focused / Competitor migration:** `+10%`.
  * **Standard commercial inquiry:** `0%`.
  * **Budget-sensitive / Price-shopping / Tender:** `-15%`.

*Special Hard Rules:*
- If volume <= 30 shipments/mo and the company is from G20 or Enterprise, price is strictly **$4.00 PAYG / $3.00 Annual**.
- Calculated unit rates must never breach the absolute bounds: [$0.60 – $4.00 for PAYG, $0.45 – $3.00 for Annual].

---

## 💡 Step 3: Additional Value Drivers & Guardrails (Senior Sales Rules)

1. **Minimum Monthly Commitment ($50/mo Floor):**
   * Even if a client tracks 5 shipments at $4.00 ($20), the minimum invoice is **$50.00 / month** (or $500/year) to cover processing and infrastructure.
2. **API Fair-Use Call Ratio:**
   * 1 unique shipment includes up to **30 API status polling calls** (or real-time webhooks).
   * High-frequency scraping (>100 calls/shipment) requires an enterprise infrastructure surcharge.
3. **Air Cargo (AWB) Tracking:**
   * Covered within the same unified contract.
   * If Air Cargo exceeds 30% of total volume, quote Air AWBs at standard rate + 10-15% due to higher upstream airline data costs.
4. **Multi-Product Bundle Discount:**
   * When combining **Tracking + Schedules** or **Tracking + Freight Rates**, offer an additional **15% bundle discount** on the secondary module.
5. **Contract Precedence & Legal Entity:**
   * Issued via **WEMELOGISTICS LTD** (UK, Company #14081751, London).
   * Commercial Part 1 takes precedence over general T&C.

---

## 🛠️ Step 4: Python CLI Calculator

Use the executable CLI tool for instant mathematical evaluations:
```bash
python /opt/hermes/profiles/richard/scripts/pricing_calculator.py --country "Germany" --employees 150 --revenue 5.0 --shipments 2000 --appetite "normal"
```

---

## 💬 Step 5: Sales Proposal Presentation Framework & Negotiable Levers

When presenting recommendations to the sales rep:
1. **Provide the 3-Tier Negotiation Range:**
   - **Opening Offer (Anchor):** Target + 15% (gives room to concede).
   - **Target Price (Fair Value):** Ideal price to close the deal.
   - **Walk-Away Floor:** Lowest acceptable rate without escalation to Stefan.
2. **Side-by-Side Comparison:** Always present PAYG vs. Annual Prepay to incentivize upfront cash flow (-25% discount).
3. **MANDATORY: Frame Pricing as Negotiable (Негошиебл-рычаги):**
   * Emphasize to the rep that the client must never perceive the quote as a rigid wall.
   * Give the rep clear trade-off levers to offer the client in exchange for discounts:
     - **Годовой контракт (Annual Prepay):** Гарантированная скидка 25% при оплате вперед.
     - **План роста объемов (Tiered Milestones):** Снижение унитарной ставки автоматически по мере увеличения числа отгрузок.
     - **Бандл (Multi-Product):** Скидка 15% при подключении расписаний (Schedules) или ставок фрахта (Rates).
     - **Оптимизация API:** Переход на Webhooks вместо тяжелого поллинга снижает нагрузку и дает лучшую ставку.
     - **Маркетинговая уступка:** Разрешение на публичный кейс-стади или логотип на сайте Navo24.
4. **Draft Client Pitch Script:** Provide a ready-to-use message snippet for the manager to paste into email or WhatsApp.
