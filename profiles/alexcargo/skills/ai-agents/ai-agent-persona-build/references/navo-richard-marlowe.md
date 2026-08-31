# Navo24 / Richard Marlowe — knowledge bank
*Condensed from the Richard Marlowe build (navo24.com + competitors). Reuse for any ocean-freight / logistics sales agent, or when extending Richard.*

## Navo24 positioning
"Ocean-freight intelligence your software can call directly. Four instruments. One spine. Never dark."
Four **MCP-native** components on one shared data spine, delivered 3 ways: **MCP tools** (AI agent calls directly), **REST API** (one key), **HMAC webhooks** (push). Each standalone with its own free tier.

## The 4 products (cite these numbers — they are MEASURED, not marketed)
- **TrackingMCP** (trackingmcp.com): container visibility, **234 carriers** (121 direct connectors, 186 SCACs), events normalised to **DCSA**, ETAs *predicted from observed delay* (never "100% complete" on an un-sailed box), demurrage & detention free-time, port congestion, AIS vessel positions. **0–5 min** event freshness. **2–3 independent data paths per carrier, auto-failover → never dark.** Self-healing connectors.
- **SchedulesMCP** (schedulesmcp.com): point-to-point, **5,000+ lanes, 255 ports, 72,000+ forward sailings**, vessel-first cards (carriers sharing a hull = one card), reliability from *observed arrivals*.
- **LoadingMCP** (loadingmcp.com): 3D load planning to **CTU Code, IMDG** segregation, **EN 12195** lashing, axle/floor limits, centre-of-gravity. "3D packing that explains itself."
- **FreightRatesMCP** (freightratesmcp.com): live ex-Asia spot rates (20'/40'/40HC), **daily rate trend**, on-time per lane from observed arrivals, one-click firm quote to vetted forwarder.

Spine logic: 01 Schedules (pick sailing) → 02 FreightRates (price lane) → 03 Loading (plan box) → 04 Tracking (watch). Adopt one; add rest later. No migration.

**Free tier (TrackingMCP): 5 active containers, 100 MCP/API calls/mo, no card, never expires.** Public no-login tracker at trackingmcp.com/track.

## Tool names (for function-calling schemas)
add_container, get_container_detail, get_shipment_summary, get_demurrage_free_time, get_demurrage_report, get_port_congestion, get_vessel_position, find_sailings, compare_sailings, get_lane_reliability, get_vessel_rotation, plan_load, check_compliance, get_load_plan, export_load_plan, get_lane_rate, get_rate_index, get_rate_trend, request_quote.

## Competitors (honest comparison — a feature, not a tone choice)
- **SeaRates.com** (main rival): UK platform (est. 2005), under **DP World** since 2023. 20+ tools (Logistics Explorer, Container/Air/Rail/Road/Parcel Tracking, Schedules, Load Calculator, Route Planner, Freight Index, Booking, Logistics Map, Mobile App, Cargo Wizard, **SeaRates AI**, Vessel Tracking). Strengths: broad multimodal, public widget, rate discovery in one place, DP World backing, trade finance. vs Navo: typically one data path/source (no 2–3 fallback), **no first-party MCP server**, **API access quote-only** (no self-serve free tier), no schedule-enriched ETA overlay, DCSA not a differentiator. → Tell client honestly: SeaRates wins if they want a broad storefront + aren't building an AI agent; Navo wins for MCP-native, DCSA-clean events, published D&D free-time, one-component wiring.
- **project44**: broad enterprise visibility, enterprise pricing → Navo: composable, self-serve, no sales cycle.
- **Terminal49**: polished US-import tracking + demurrage, API-first, free tier → Navo: +schedules +loading.
- **Vizion API**: developer-first, closest philosophy, no free tier → Navo: MCP, truthful ETAs, schedules+loading spine, free tier.
- **GoComet**: freight mgmt + predictive → Navo: MCP-native for builders, public free-time, no-login demo.
- **Flexport / Kuehne+Nagel / CargoWise**: enterprise 3PL/TMS → Navo is components they can embed.

## Retell AI (voice) — key facts for wiring
#1 AI voice agent platform; connects to any telephony via **SIP Trunking**; inbound+outbound; ~800ms latency; proprietary turn-taking (handles interruptions); binds any LLM (GPT/Claude) so the agent can be the voice; post-call analysis + sentiment; partners Twilio/Vonage/n8n; phone number ~$2/mo + pay-as-you-go minutes. Docs: docs.retellai.com.

## Hard guardrails (bake into any freight agent)
- Don't promise out-of-scope: no rate procurement (SeaRates), no multimodal rail/road (Terminal49), no enterprise TMS (CargoWise).
- Don't fabricate ETA/data — "no carrier data" is shown as itself.
- Don't spam/pressure. Don't disclose Navo confidential info outside NDA.
- Escalate legal/financial/contract/signing to a human ("the desk").
