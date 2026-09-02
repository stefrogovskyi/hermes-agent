# Technical Trial Feedback, Gateway Handling & Team Escalation Playbook

Standards for handling in-depth technical trial evaluations, carrier error diagnostics, pricing separation, and peer escalation in Navo24 B2B sales.

## 1. Strict Zero Fabrication Policy

When prospects or trial users submit technical inquiries regarding:
- HTTP status codes (502 Bad Gateway, 504 Gateway Timeout)
- Carrier data latency or background processing
- DCSA event taxonomy or milestone classification anomalies
- Vessel rollovers and schedule revisions
- API endpoints and documentation gaps
- Third-party references (GoComet, SeaRates legacy tags)

**NEVER invent or synthesize technical explanations, backend architecture details, or error root causes.**
If an exact answer is not verified by official docs or the core engineering team:
1. STOP and acknowledge what needs verification.
2. Escalate directly to the engineering team via the internal Telegram group.
3. Formulate the client response ONLY after receiving confirmed technical facts.

## 2. Internal Telegram Group Escalation Standard

When presenting client trial feedback to developers and leadership (Eugene Karavan, Alexey Shatunov, Stefan Rogovskiy):
- Use a natural, peer-to-peer conversational tone.
- **NO decorative header lines** ("Обозначающие тему" introductory sentences).
- **NO spammy emojis or corporate boilerplate**.
- Present facts directly as concise bullet points:
  - Exact container / B/L numbers.
  - Observed error codes, latency, and behavior.
  - What the client actually asked.

### Canonical Internal Message Pattern:
```text
Всем привет еще раз, у меня фидбек по триалу от клиента. Он протестировал API на 5 своих контейнерах и 5 индийских маршрутах расписаний. Очень доволен детализацией мультимодальных перегрузок, но вот такие вопросы возникли:

- Maersk 274209874 словил 504 Gateway Timeout (104 сек)
- CMA CGM AMC2589041 словил 502 Bad Gateway (79 сек)
При этом через 3 минуты оба контейнера нормально появились в базе. Клиент спрашивает почему синхронный вызов завис, списались ли эти вызовы с квоты и как правильно делать регистрацию (POST 202 vs GET).

На контейнере CMA CGM AMC2619449 был перенос (ролловер) с APL PARIS на CMA CGM SAIGON, а API показал текущий статус без маркера ролловера и истории смены судна. Можно ли отдавать историю рейсов/флаг rollover?

На HMM BOME86970700 гейты (gate-in/gate-out) смапились в transport departure/arrival до погрузки на судно. Клиенту нужно точное разделение интермодальных гейтов от морских этапов.

Nhava Sheva -> Jeddah (65 рейсов) и Mundra -> Dar es Salaam (24 рейса) отработали отлично.
А вот на направлениях из Nhava Sheva в Shuwaikh (Кувейт), Oran (Алжир) и Pointe des Galets (Реюньон) вернулось 0 результатов. Просит уточнить, это ограничение окна дат или отсутствие фидерных стыковок?

Клиент заметил метки GoComet и SeaRates в метаданных источников и спрашивает про независимость инфраструктуры Navo.
```

## 3. Verified Backend Architecture & Operational Facts

Based on direct confirmation from Navo24 engineering leadership:

### Gateway Timeouts (502 / 504) on Registration
- **Cause**: Ocean carrier portals (e.g. Maersk, CMA CGM) occasionally experience high latency during initial direct connector queries, causing the client HTTP gateway connection to time out (70–110s).
- **Background Worker**: Navo's asynchronous worker queue keeps processing the carrier response in the background. As soon as the carrier responds, the shipment is indexed and available via subsequent lookups.
- **Quota Impact**: Failed or timed-out registration requests do NOT consume the client's trial or paid allowance.

### Quota Consumption Logic (Lookups, Rechecks, Webhooks)
- **Automated Carrier Rechecks**: 0 API calls consumed (performed automatically on Navo backend).
- **Webhook Event Deliveries**: 0 API calls consumed (included in the subscription at no extra charge).
- **Direct Lookup Requests (GET)**: Consume API calls from the monthly allowance (e.g., 750 calls/month pool), but repeated lookups for the same container within the same calendar month do NOT count as an additional unique shipment.

### Vessel Rollovers
- Ocean carrier direct operational feeds do NOT publish rollover markers or former/revised vessel histories. Navo reflects the live operational vessel published by the line.

### DCSA Event Mapping
- Mapping anomalies (such as inland gate moves appearing as transport departure/arrival prior to vessel loading on carriers like HMM) represent internal mapping issues that are logged and patched by engineering.

### Schedules Coverage & Niche Lanes
- If a route returns 0 sailings (e.g. India to Shuwaikh, Oran, Pointe des Galets), active carrier feeds have no published schedules for those feeder ports.
- **Sales Response Strategy**: Ask the client which specific carriers they use on those corridors; the Navo engineering team will integrate and add those carrier feeds directly for their workflow.

### Data Independence & Legacy Mentions
- All tracking and schedule feeds are native and independent.
- Mentions of GoComet or SeaRates in metadata are legacy output serialization artifacts, actively being removed by dev.

### Product Separation in Pricing
- **Container Tracking API**: USD 50/month (or USD 500/year) covers up to 25 unique shipments and 750 API calls.
- **Ocean Schedules API**: Billed SEPARATELY based on monthly request volume. NEVER bundle them into a single $50 rate without specifying separate schedule call volumes. Always ask the client for expected monthly schedule call volume before proposing the schedule plan.
