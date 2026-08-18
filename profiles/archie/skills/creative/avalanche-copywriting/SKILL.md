---
name: avalanche-copywriting
description: "Humanized anti-AI copywriting for Avalanche Agency."
version: 1.0.0
author: Archie Wright
metadata:
  hermes:
    tags: [writing, copywriting, avalanche, anti-ai, humanizer, content]
    category: creative
---

# Avalanche Agency Copywriting & Humanization Standard

Guidelines and workflows for writing non-detectable, engaging, human content for Avalanche Agency (Аваланч Ейдженси) clients.

## Core Rules & Anti-AI Directives

1. **Strict Prohibition of Em-Dashes (Длинное тире —):**
   - Do NOT use `—` (em-dash) or `--`.
   - Use natural sentence structures, commas, parentheses, or separate sentences instead.
   - This includes meta-title and meta-description, not just body text. Check them separately during self-audit.

2. **Elimination of AI Clichés & Slop (АИ-калька и канцелярит):**
   - Strip AI marker words and phrases: *несомненно, важно отметить, ключевой аспект, в современном мире, погрузиться, неотъемлемая часть, уникальный баланс, это не просто X, а Y, подвести итог, следует подчеркнуть*.
   - Avoid empty intro/outro filler ("В этой статье мы рассмотрим...", "В заключение можно сказать...").
   - Remove pseudo-profound participle phrases ("подчеркивая значимость...", "обеспечивая тем самым...").

3. **Fresh, Non-Standard Style (Нестандартные обороты):**
   - Use unexpected, vivid vocabulary, conversational idioms, metaphors, and sharp narrative angles fitting the target genre/industry.
   - **But ration metaphors: 1-2 strong images for the WHOLE article, not one per section.** A metaphor in every paragraph is itself an AI tell — real writers save the vivid image for one or two moments and stay plain everywhere else.
   - Mix sentence lengths dramatically: punchy short thoughts followed by natural, flowing explanations.
   - Inject genuine voice: author opinions, realistic examples, nuanced reasoning.

4. **Bypassing AI Detectors (АИ-детекторы):**
   - High perplexity and burstiness: vary vocabulary, paragraph lengths, and structural rhythm.
   - Avoid balanced rule-of-three lists (`A, B и C`).
   - Avoid mechanical bolding/bullet formatting unless explicitly requested.

5. **Break the "Textbook Architecture" (структурная регулярность):**
   - A rewrite that maps cleanly onto "why it matters → what goes wrong → how to fix it technically → how to drive adoption → bonus value → industry trend → practical checklist" reads as AI-generated even if every sentence is original, because real subject-matter writing rarely walks a perfectly logical staircase.
   - Deliberately break the chain at least once: let one section open mid-thought instead of with a topic sentence, let one point sit slightly out of "ideal" order, allow one paragraph to be a genuine tangent or a specific anecdote that doesn't perfectly set up the next section.
   - Vary section length hard: some sections should be one short paragraph, others three. Uniform section length is itself a tell.
   - **Reordering sections is not enough on its own.** Even a reshuffled piece can still read as "problem → context → mechanics → adoption → bonus value → rules", i.e. a recognizable content-marketing template, just with the boxes moved around. The real fix is to occasionally merge two ideas into one section instead of giving each its own heading, or let a section end without a tidy practical payoff, or drop a transition entirely so two sections sit side by side without the connective bridge a marketing outline would insert. The goal is a piece that feels like it was written by someone thinking through the subject, not one assembled from a content brief.

6. **Ban Over-Explaining Connectors ("That's why..." chains):**
   - Do NOT let every sentence perfectly justify the next one with explicit connective tissue: *"That's why...", "Which is why...", "That's a sign of...", "Retrieval is where most operations quietly fall apart"*-style declarative mini-verdicts stacked one after another.
   - A human writer leaves some causal links implicit. Cut at least half of the explicit "X, that's why Y" / "which explains why Y" connectors a first draft produces; let the reader infer some of them.

7. **Limit Contrastive Negation ("X, not Y" / "It isn't X, it's Y"):**
   - This construction in ANY direction (*"not a documentation gap, it's a filing problem"*, *"not reconstructed from memory"*, *"not better at arguing, they just..."*, *"instead of dueling accounts"*) is one of the strongest LLM tells there is.
   - Hard limit: **maximum ONE such construction in the entire article.** Audit by literally grep-ing for " not " used contrastively and for "instead of" — if there are 3+, cut down to 0-1.

8. **Avoid Aphoristic, Quotable Sentences on Every Beat:**
   - If nearly every paragraph ends on a crisp, tweetable one-liner ("Once photos are searchable, they earn their cost more than once."), that polish density is itself suspicious. Real professional writing has flatter, more workmanlike sentences mixed in — not every thought needs a punchy landing.
   - Deliberately leave 2-3 sentences per article slightly less polished or slightly more matter-of-fact than your instinct suggests.
   - **This applies to mid-paragraph "hook" sentences too, not just section endings.** A sentence visibly built to be memorable or literary in the middle of otherwise plain prose (e.g. "Somewhere in that six-figure pile sits the one photo that would settle a shipment's dispute in an afternoon") is a tell even when it isn't a section-closer. Allow yourself exactly ONE crafted, literary-feeling sentence in the entire piece, ideally the opening line. Every other sentence should read like it was written to convey information, not to be quoted.

9. **No Parallel Twin-Sentence Conclusions:**
   - Avoid closing a section with two structurally mirrored sentences ("Evidence both sides trust closes a claim in days. Evidence one side can pick apart drags on for weeks.") — this call-and-response parallelism is a classic AI cadence. Collapse it into one sentence or break the parallel structure entirely.

10. **Ban Symmetric Antithesis Pairs, Even Without "Not":**
    - The mirrored-sentence tell in rule 9 also shows up in subtler form WITHIN a sentence or two, without any explicit negation word: matched vocabulary sets standing in deliberate opposition ("trust... picking apart", "close... drag", "days... weeks"). This is the same LLM cadence as rule 9, just compressed and without a "not" to grep for.
    - When editing a conclusion or transition, check whether you've built a matched pair of opposites (positive-state/negative-state, short-timeframe/long-timeframe, verb-that-builds/verb-that-breaks) dressed up as parallel grammar. If so, break the symmetry: cut one half, change the sentence structure so the two ideas don't mirror each other, or state the second idea as a flat fact instead of an echo of the first.

11. **No Fabricated Facts or Invented Claims (Недопустимость выдуманных фактов):**
    - Rewriting for style must NEVER introduce claims, mechanisms, numbers, or causal explanations that are not present in and not directly inferable from the source article. This is a factual-integrity rule, separate from the anti-AI-detection rules above, and it applies with extra force to release notes, changelogs, product updates, and any factual/news-style content.
    - The most common failure mode: the writer, reaching for "unique stylistics" (rule 3) or trying to sound like a subject-matter expert, invents plausible-sounding technical detail that was never stated by the source. Real example caught in production: a SeaRates changelog entry saying carriers were added to tracking got rewritten to also claim this improves "predictive ETA models" and "exception detection" and helps avoid "demurrage and detention charges" - none of which the source said. This reads as confident, expert, on-brand copy, and is completely fabricated.
    - Test before finalizing: for every concrete claim, mechanism, or benefit stated in the rewrite, can you point to the exact sentence in the source that supports it? If not, cut it or rephrase it as an obvious, source-supported inference only ("more carriers means less need to check separate portals" is fine if the source lists more carriers; "this improves exception detection algorithms" is not fine unless the source says so).
    - Stylistic elaboration is allowed (tone, structure, framing, sentence rhythm); factual elaboration is not (new numbers, new mechanisms, new named benefits, new causal claims).
    - This check must be added explicitly to the Step 7 independent audit (a 4th layer alongside plagiarism, word-level AI tells, and structural AI tells) and to the Step 8 self-audit.

## Workflow for Content Creation (8-Step Process)

This workflow incorporates advanced steps for humanized, SEO-optimized, and AI-audit-proof content.

1. **Complete Text Ingestion (Полное считывание текста):**
   - Fully read and understand the source article from SeaRates.

2. **Deep & Meaning-Preserving Rewrite (Полный рерайт):**
   - Rewrite the entire text, maintaining its original volume, meaning, and core essence.
   - Crucially: generate a *new, unique, and SEO-optimized title* (max 60 chars), *meta-title* (max 60 chars), and *meta-description* (max 160 chars) – these must be rephrased, not copied.
   - Avoid any direct copying or simple paraphrasing from the original. The rewrite must be 100% original human-sounding prose.

3. **Inject Unique Style & Original Turns of Phrase (Добавление уникальной стилистики):**
   - Actively infuse the text with distinct human voice, creative idioms, metaphors, and varied sentence structures (high perplexity, high burstiness).
   - Adhere strictly to anti-AI directives: no em-dashes, no AI clichés (e.g., "важно отметить", "в современном мире"), no pseudo-profound participle phrases.

4. **Trend-Based Keyword Analysis (Анализ трендовых ключевых слов):**
   - Perform targeted `web_search` queries to identify current and trending keywords relevant to the article's topic.
   - Integrate these keywords naturally and contextually throughout the rewritten text, aiming for organic flow rather than keyword stuffing.

5. **Keyword Compliance Check (Проверка на соответствие ключевым словам):**
   - Review the drafted text to ensure effective and natural incorporation of identified trending keywords.
   - Verify that keyword usage enhances readability and SEO value without sounding forced.

6. **Text Refinement Post-Keyword Analysis (Доработка текста по ключевым словам):**
   - Make necessary adjustments to the text based on the findings from Step 5, optimizing for both human readability and search engine relevance.

7. **Independent AI Audit Pass (Независимый ИИ-аудит):**
   - **Delegate a sub-agent to act as an independent auditor.** Give it ONLY the original source and the rewrite (not the author's self-report of what it fixed) so it audits fresh, without anchoring on the writer's own claims.
   - The auditor must check, explicitly and separately, FOUR layers, not just one:
     a) **Plagiarism/similarity** — sentence-by-sentence comparison against the original, flagging any 6+ consecutive word overlap beyond industry-standard terms or proper nouns (company/product/carrier names are exempt).
     b) **Word/phrase-level AI tells** — em-dashes, cliché phrases, banned intro/outro filler.
     c) **Structural/rhetorical AI tells** — this layer is commonly missed and must be checked on its own pass: does the section order form a too-perfect logical staircase (why it matters → problem → fix → adoption → bonus value → trend → checklist)? Are section lengths suspiciously uniform? Count instances of explicit "That's why / which is why" causal connectors. Count contrastive "X, not Y" / "instead of" constructions. Count how many paragraphs end on a crisp, aphoristic one-liner. Flag any parallel twin-sentence conclusions ("Evidence both sides trust closes X. Evidence one side disputes drags Y.").
     d) **Factual fabrication** — for every concrete claim, mechanism, number, or named benefit in the rewrite, check it traces back to something the source actually says. Flag any invented technical detail, causal explanation, or benefit that sounds plausible and on-brand but isn't supported by the source. This is especially critical for release notes / changelog / product-update style content.
   - The auditor must return concrete counts and quoted examples for each layer, not a vague impression, and a clear PASS/NEEDS-WORK verdict per layer.

8. **Final Refinement Post-Audit (Финальная доработка после аудита):**
   - Incorporate feedback and address issues identified during the independent AI audit (Step 7) to produce the highest quality final version.
   - Perform a final self-audit to ensure all core rules and anti-AI directives are met before publication, INCLUDING the structural/rhetorical checks in 7c and the factual-fabrication check in 7d, not just word-level clichés.
   - **Never trust a sub-agent's self-report of what it fixed at face value.** After any rewrite or revision pass, independently re-run the mechanical checks yourself (grep/count em-dashes, count "X, not Y" constructions, run an n-gram overlap check against the original source) before marking the article as done. Revision passes frequently reintroduce new overlaps with the original or leave banned patterns behind even while claiming full compliance. For factual content, also re-read the rewrite side by side with the source and manually verify no claim, mechanism, or benefit was invented.
