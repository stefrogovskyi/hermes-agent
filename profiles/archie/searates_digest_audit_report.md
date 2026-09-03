# Audit Report — SeRates Dec 2025 Digest Rewrite
Source: original digest vs `/opt/hermes/profiles/archie/searates_digest_dec2025_rewrite.md`

## (a) Plagiarism / similarity — verdict: NEEDS-WORK (minor)

6+ consecutive-word overlaps found:

1. **"reduce dependence on the US market and open new corridors"** (rewrite §2, line 33) vs original "to reduce dependence on the US market and open new corridors in…" — **10-word verbatim run**. Clearest flag.
2. **"procurement teams, shippers, manufacturers, and carriers"** (line 21) vs original "for procurement teams, shippers, manufacturers, and carriers" — exact 7-word match. Not proper nouns (role lists), so technically flaggable, though low-severity boilerplate.
3. Borderline (5 words, watch-list): **"capacity availability, and environmental performance"** (line 95) vs original "capacity availability, and environmental performance are now key…".

Exempt/clean: "Comprehensive Economic Partnership Agreement with Oman" (treaty proper noun), "Logistics Explorer tool", "CO₂ Calculator", place/carrier names. No other 6+ runs detected; the prose is otherwise genuinely rewritten.

## (b) Word-level AI tells — verdict: PASS (with notes)

- Em-dashes (—) / double hyphens (--): **0** in body. Clean.
- Cliché phrases ("it's important to note", "in today's world", "dive into", "in conclusion"): **0**. Clean.
- "not just X" pattern: **2 instances** — "not just another policy announcement" (line 17), "not just quote prices" (line 67). Under "overuse" threshold but worth pruning one.
- Pseudo-profound participles: essentially none; "rewriting global supply chains" in meta-description is mild marketing voice.

## (c) Structural / rhetorical AI tells — verdict: NEEDS-WORK

- **Causal connectors**: "That is why" (line 51), "This is exactly why" (line 55) → **count: 2**. One should be cut.
- **Contrastive "X, not Y" constructions**: **count: ~5** (limit: 1). Instances:
  1. "'It has always been reliable' is no longer a strategy. It is a liability." (It-is-not-X.-It-is-Y form, line 11)
  2. "The issue is often not paying too much for freight. It is finding available capacity at all" (lines 51–52)
  3. "pricing on current reality, not last quarter's numbers" (line 45)
  4. "explain environmental impact to customers, not just quote prices" (line 67)
  5. "as a tool for managing risk, time, and growth rather than a line item to minimize" (line 95)
  → **Hard fail on the ≤1 limit.**
- **Aphoristic one-liner paragraph endings**: **~5** — "…is how you lose." (55), "It is a liability." (11), "They decide who wins contracts." (61), "now is a good time to look again" setup ending "beating rock-bottom freight rates." (89), "current reality, not last quarter's numbers" (45). Too many; reads as engineered punchiness.
- **Parallel twin-sentence conclusions**: line 11 ("no longer a strategy. It is a liability.") and line 61 ("no longer marketing language. They decide who wins contracts.") — same two-beat template used twice.
- **Symmetric antithesis pairs**: "a competitive edge or a wall" (line 65) — mirrored-opposite framing; plus the strategy/liability pair above.
- **Uniform lengths / template**: sections follow an identical skeleton (2–3 paragraphs + "Why it matters:" + 3 emoji-bulleted stakeholder lines, 🚢🧭💼 rotated). Mechanically parallel; consider varying at least one section.
- **Logical staircase**: section order simply mirrors the source article's own order (Hainan → India → $35T → green → Mexico), so it isn't an AI-invented staircase; the intro→five-sections→sum-up arc is inherent to digests. Not flagged.

## (d) Factual fabrication — verdict: NEEDS-WORK (small number of inventions)

Everything else traces: Dec 18 Hainan customs launch ✓, DHL Express APAC personnel changes ✓, CEPA with Oman + EU/NZ/Chile talks ✓, textiles/pharma/auto/e-commerce ✓, GCC hub demand ✓, UNCTAD $35T record 2025 ✓, uneven growth / capacity-vs-cost problem ✓, slot shortages & port congestion vs unstable volumes/rates ✓, diversification advice ✓, $78.9B green logistics by 2030 ✓, decarbonization as KPI ✓, CO₂ Calculator A/B inputs, emissions+offset+carrier comparison, blog guide, offsets in SeaRates.com bookings and Logistics Explorer ✓, Maersk Manzanillo depot + cost/transit benefits ✓, regional-hub shift, US/Canada capacity expansion ✓, all five conclusion points ✓.

Invented / escalated details:
1. **"one of the largest free trade zones anywhere"** (line 17) — original says only "large-scale free trade zone"; superlative ranking is fabricated.
2. **"The Hainan Free Trade Port"** (line 17) — official program name not present in source (source: "free trade zone"); also "island-wide customs closure" and meta-description's "customs closure" introduce terminology absent from the original (defensible real-world term, but unverifiable against the given text).
3. **"They decide who wins contracts."** (line 61) — new causal claim; original says ESG is a KPI, never that green credentials determine contract awards.
4. **Contact closer** (line 97): "find the most profitable route and keep your logistics transparent end to end" — invented benefit promises; original merely lists the sales email.
5. Minor: "negotiating hard with the EU…" adds intensity beyond "confirmed active negotiations"; "rates swinging in both directions" slightly dramatizes "fluctuating rates."

## Summary verdicts
| Layer | Verdict |
|---|---|
| (a) Similarity | NEEDS-WORK — one clear 10-word verbatim run + one 7-word role-list match |
| (b) Word-level tells | PASS — zero dashes/clichés; trim "not just" ×2 |
| (c) Structural tells | FAIL — 5 contrastive constructions (limit 1), 2 causal connectors, 5 aphoristic endings, templated sections |
| (d) Fabrication | NEEDS-WORK — 3–4 invented claims (largest-zone superlative, "wins contracts", contact-line promises, FTZ naming) |

Recommended fixes: reword the §2 corridor sentence; delete or invert 4 of the 5 contrastive constructions and 2–3 punchy closers; soften "one of the largest…anywhere"; cut or ground "They decide who wins contracts"; strip the invented promises from the closing contact line.
