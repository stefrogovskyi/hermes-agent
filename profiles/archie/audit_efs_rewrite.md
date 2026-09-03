# Independent QA Audit: "Emergency Fuel Surcharges in 2026" Rewrite

## (a) PLAGIARISM / SIMILARITY — VERDICT: NEEDS-WORK (minor, 1 clear violation)

Method: sentence-by-sentence comparison, excluding exempted terms (BAF, FSC, EFS, TEU, Bunker Adjustment Factor, SeaRates, Platts, IATA, Brent crude, Load Calculator, Container Tracking).

**Violation found (≥6 consecutive words, not fully covered by exemptions):**
- Original: "An emergency fuel surcharge (EFS) **isn't a** tax or a regulatory toll"
- Rewrite: "An emergency fuel surcharge (EFS) **isn't a** government tax or a fixed toll."
- Consecutive match: "An emergency fuel surcharge (EFS) isn't a" = **7 words**. The term "emergency fuel surcharge (EFS)" is exempt, but the wrapper "An … isn't a" is copied structure, not just terminology — this is the definitional opening sentence reused almost verbatim with only "tax"→"government tax" and "regulatory"→"fixed" swapped. **Recommend rewording this specific clause.**

**Near-miss / borderline paraphrases (5 words, under threshold but flagged for awareness — pattern of very tight paraphrasing around factual lists):**
- "a **flat fee per shipment, per container**, or per kilogram" vs original "a **fixed fee per shipment, per container** (TEU), or per kilogram" — 5-word identical run.
- "pressured **carriers to raise surcharges to** keep operations" vs original "leading **carriers to raise surcharges to** sustain service" — 5-word identical run (FAQ 4).
- "**global energy volatility and** disruptions" vs original "**global energy volatility and** route-related risks" — 4-word identical run (FAQ 4).
- "a **pricing adjustment mechanism**" appears verbatim in both FAQ 1 answers (4-word run).
- "**monthly or even weekly**" identical in both (Air freight section) — 4-word run.

**Everything else** (invoice term lists, negotiation bullets, audit checklist bullets) reuses only exempted acronyms/terms (EFS, FSC, BAF, Platts, IATA) — fine.

**Verdict: NEEDS-WORK** — one clean 7-word violation on the core EFS definition sentence; a cluster of 4–5 word near-verbatim runs elsewhere suggests the paraphrase engine leaned on light word-swapping rather than full resynthesis in a few spots. Not pervasive, but the definition sentence should be rewritten.

---

## (b) WORD/PHRASE-LEVEL AI TELLS — VERDICT: PASS

- **Em-dash (—) count: 0.** Double-hyphen (--) count: 0. Checked title, meta-title, meta-description, and full body — none found.
- **Banned cliché list check:** "it's important to note" (0), "in today's world" (0), "delve into" (0), "seamless" (0), "robust" (0), "unlock" (0), "landscape" (0), "realm" (0), "testament to" (0), "plays a crucial role" (0), "not just X but Y" (0). **All zero.**
- Minor secondary observations (not on the banned list, but worth a note): repeated hedging/meta-transition tics — "Worth noting, …", "Worth checking before you sign anything, **honestly**", "**Also worth flagging** before we get into disputes" — these are softer, non-listed filler patterns typical of "casualized" AI copy. Not disqualifying under the stated rubric, but flagged for polish.

**Verdict: PASS** on all required (b) criteria (0 dashes, 0 cliché phrases from the list).

---

## (c) STRUCTURAL/RHETORICAL AI TELLS — VERDICT: NEEDS-WORK

- **Section order:** Mirrors the original's own staircase (definition → modes → calculation model → benchmark source → invoice appearance → negotiation → audit → close → FAQ). This structure is inherited from the source article itself rather than newly invented, so it's a lower-priority concern, but it means the piece still reads as a beat-for-beat outline match to the original.
- **Section length uniformity:** Reasonably varied — roughly 90–180 words per section (shortest: "Where this leaves you" ~90 words; longest: "Three ways carriers actually calculate the number" ~180 words). Not suspiciously uniform. **No flag.**
- **"That's why / which is why" causal connectors: 0.** None found anywhere in the piece.
- **Contrastive "X, not Y" / "instead of" / "rather than" constructions: 2 found (max allowed = 1) → FLAGGED, exceeds limit:**
  1. "**Rather than** absorbing the whole hit themselves, ocean lines, airlines, and trucking companies pass a slice of that volatility onto shippers…"
  2. "…it gets applied after booking **rather than** at the time of quote, which is where a lot of billing disputes start."
- **Concessive "though" tic:** 2 instances ("though it also means invoices can shift without much warning…"; "…though they take real effort to parse.") — not part of the strict rule but a recurring rhetorical crutch worth noting.
- **Paragraphs ending on a crisp aphoristic one-liner:** Not "nearly every" section, but a notable minority (3 of 8 sections) end on a symmetric antithesis/aphorism — flagged per the specific pattern the brief calls out:
  1. "**Different names, same type of charge** showing up under different acronyms depending on the carrier." (parallel antithesis: different…same)
  2. "**None of this guarantees you win** a dispute, **but it puts you in a far stronger position** than showing up empty-handed." (matched opposition: guarantee/win vs. stronger position/empty-handed)
  3. "Together they **won't stop** fuel prices from moving, **but they make** the resulting costs far easier to see coming and plan around." (won't-stop vs. make-easier antithesis)
  
  These are the exact "symmetric antithesis pair" pattern the brief warns about (cf. its own example "trust…picking apart").

**Verdict: NEEDS-WORK** — exceeds the allowed contrastive-construction count (2 vs. max 1), and contains 3 clear symmetric-antithesis closing lines that read as a stylistic tic rather than organic variation.

---

## (d) FACTUAL FABRICATION (CRITICAL) — VERDICT: NEEDS-WORK (1 flagged fabrication)

Checked every concrete claim, mechanism, number, named index/entity against the original:

- All acronyms/definitions (EFS, BAF, FSC), the three fuel-surcharge modes (ocean/air/road), the three calculation models (index-based, fixed add-on, contract/dynamic), the benchmark indices (Brent crude, Platts, IATA fuel indices, regional diesel trackers), the invoice term list (EFS, FSC, BAF, energy adjustment, fuel recovery fee), the negotiable/non-negotiable items (cap/collar, review rhythm, benchmark clarity, effective date; crisis-driven surcharges), and the audit checklist/documentation list all **trace cleanly to explicit original sentences.** No invented numbers, percentages, dollar figures, or carrier names were introduced anywhere.

**Flagged fabrication:**
- Rewrite (audit checklist section): "Confirm the timing too, booking versus departure. **This single detail causes more billing arguments than almost anything else on this list.**"
- Original only says: "Application timing test (verify whether fees apply at booking or departure, avoiding billing blur or backdated bumps)." — it never ranks this as causing the *most* disputes relative to the other checklist items. The superlative claim ("more … than almost anything else on this list") is an **invented comparative/statistical assertion with no source basis** — exactly the kind of fabricated emphasis the brief flags as highest priority, since this is factual/educational release-notes content.

Minor (non-critical) embellishments worth noting but not rising to fabrication:
- "isn't a **government** tax or a **fixed** toll" — original just says "tax… regulatory toll"; small unsupported specificity added ("government"), low severity.
- "invoices can shift without much warning, **which is just part of how the system works now**" — an editorializing generalization; loosely supported by the original's booking-vs-post-departure point but stated with more certainty than the source.

**Verdict: NEEDS-WORK** — one clear invented superlative/statistic-style claim must be removed or hedged before publication; everything else in the rewrite is factually traceable to the original.

---

## Summary Table

| Layer | Verdict | Key issue count |
|---|---|---|
| (a) Plagiarism/Similarity | NEEDS-WORK (minor) | 1 clear 7-word violation; 5 near-miss 4–5 word runs |
| (b) Word/Phrase AI Tells | PASS | 0 dashes, 0 cliché phrases |
| (c) Structural/Rhetorical AI Tells | NEEDS-WORK | 2 contrastive constructions (max 1); 3 antithesis closers; 0 "that's why" |
| (d) Factual Fabrication | NEEDS-WORK | 1 invented superlative claim (critical) |

**Overall: NOT YET READY FOR PUBLICATION.** Fixes needed: (1) rewrite the EFS definition opening clause to break the 7-word overlap, (2) cut one of the two "rather than" constructions, (3) soften/remove the "more billing arguments than almost anything else on this list" claim, (4) optionally vary the 3 antithesis-style closing lines so they don't read as a repeated template.
