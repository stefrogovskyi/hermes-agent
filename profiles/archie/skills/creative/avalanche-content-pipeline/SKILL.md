---
name: avalanche-content-pipeline
description: "Use when running the recurring Avalanche content pipeline (queued articles processed automatically, no Make.com). 9-stage micro-agent process: ingest, extract, SEO brief, deep write, humanize, link/anchor, audit gate, fix loop, DOCX delivery."
version: 2.0.0
author: Archie Wright
metadata:
  hermes:
    tags: [copywriting, pipeline, anti-ai, avalanche, seo, docx, cron, automation]
    category: creative
---

# Avalanche Content Pipeline (Native, No Make.com)

This skill replaces the Make.com content pipeline with a native Hermes process.
It is designed to be run by a **recurring cron job** that processes one queue
item per tick, end to end, inside a single agent turn. No external automation
platform is involved. All 9 stages of the original architecture are covered
using tools already available in this profile.

## Architecture mapping (Make.com stage → Hermes equivalent)

| # | Make.com module | Hermes native equivalent |
|---|---|---|
| 1 | Scraper / Webhook | `web_extract` (Firecrawl-backed) on the source URL |
| 2 | Entity Extractor | Reasoning pass in this same turn: pull facts/terms/logic into a structured brief |
| 3 | SEO Enricher (Ahrefs/SerpAPI) | `web_search` for the topic + "people also ask" style queries (no paid SEO API configured — see Limitations) |
| 4 | Deep Writer (Claude 3.5 Sonnet) | This agent, running on `claude-sonnet-5` via the `anthropic` provider, writing the full draft directly |
| 5 | Humanizer & Stylist | Apply the `humanizer` skill + `avalanche-copywriting` skill rules in the same pass |
| 6 | Link & Anchor Integrator | Manual insertion pass with the spacing rule below, done as part of drafting |
| 7 | Adversarial Audit | Self-critique pass acting as a strict, adversarial editor (see Quality Gate below) — no paid AI-detector API configured |
| 8 | Fix Loop / Router | Re-run stage 5+6+7 up to 3 times until PASS |
| 9 | DOCX Generator & Delivery | `docx` skill to generate the file, then deliver via Telegram to the configured chat |

## Limitations (be upfront about these, do not fake data)

- **No DataForSEO / SerpAPI / Ahrefs key is configured.** Stage 3 uses `web_search`
  for real but shallower keyword/topic signal (actual search snippets, not
  ranked volume/difficulty data). Never invent keyword volumes or difficulty
  scores — only report what `web_search` actually returned.
- **No GPTZero / Originality.ai / CopyLeaks key is configured.** Stage 7 uses
  a strict self-critique pass by this agent acting as an adversarial editor
  instead of a third-party AI-detector score. Report the audit as
  "internal editorial review", never claim a fabricated "% AI score" — that
  number does not exist without the paid API.
- If the user adds real API keys later (`DATAFORSEO_API_KEY`, `SERPAPI_KEY`,
  `GPTZERO_API_KEY`, `ORIGINALITY_API_KEY`) to `/opt/hermes/.env`, swap the
  relevant stage to call that API via `terminal`/`curl` instead of the
  built-in fallback, and update this skill file to reflect it.

## Queue

The pipeline processes a JSON queue at:

```
/opt/hermes/profiles/archie/content_pipeline/queue/queue.json
```

Managed with the helper script:

```
/opt/hermes/profiles/archie/content_pipeline/queue_manager.py
```

Commands (run via `terminal`, from any directory — the script resolves its
own path):

```bash
python3 /opt/hermes/profiles/archie/content_pipeline/queue_manager.py add "<url_or_topic>" [--type=rewrite|topic] [--priority=N] [--notes="..."]
python3 /opt/hermes/profiles/archie/content_pipeline/queue_manager.py list [status]
python3 /opt/hermes/profiles/archie/content_pipeline/queue_manager.py next
python3 /opt/hermes/profiles/archie/content_pipeline/queue_manager.py done <id> [--output=<path>]
python3 /opt/hermes/profiles/archie/content_pipeline/queue_manager.py fail <id> "<reason>"
python3 /opt/hermes/profiles/archie/content_pipeline/queue_manager.py reset <id>
```

Item types:
- `rewrite` — source is a URL to an existing article to deep-rewrite (auto-detected from `http` prefix).
- `topic` — source is a plain topic string with no existing article to scrape (skip Stage 1 scraping, go straight to Stage 2 brainstorm using web research).

Adding to the queue can happen two ways:
1. **User in Telegram** says something like "добавь в очередь: <url>" or
   "поставь в очередь тему: <topic>" — run the `add` command with the right
   `--type`.
2. **The cron job itself** just pulls whatever is already queued — it does
   not add anything on its own.

## The 9-Stage Process (run all of this in ONE agent turn per queue item)

When triggered (by cron or manually), do the following:

### Step 0: Pull next item
```bash
python3 /opt/hermes/profiles/archie/content_pipeline/queue_manager.py next
```
If it returns `{"empty": true}`, there is nothing to do — stop here, do not
report an error, just note "queue empty" and end the turn quietly (cron jobs
should not spam the user when there's nothing to process).

If an item comes back, note its `id`, `source`, `type`, `notes`.

### Stage 1: Ingestion (skip if type=topic)
Use `web_extract` on the source URL. Strip navigation/boilerplate (the tool
already returns clean markdown). Save the raw clean text.

### Stage 2: Entity & Fact Extraction
In your own reasoning (no external call needed), extract into a structured
brief:
- `core_facts`: concrete facts, numbers, named entities (ports, document
  types, regulations, company names)
- `industry_terms`: domain vocabulary that must appear naturally
- `logical_steps`: the process/argument skeleton of the piece

For `type=topic` items, build this from general knowledge plus Stage 3
research instead of an existing article.

### Stage 3: SEO Brief
Run 2-4 `web_search` queries around the topic (main keyword + "как" / "что
такое" / "how to" / "best practices" variants relevant to the audience
language). Extract from the results:
- Recurring phrases across top results (proxy for LSI terms)
- Actual questions people are asking (from search result titles/snippets)

State plainly in your internal notes that this is directional signal from
live search results, not licensed keyword-volume data.

### Stage 4: Deep Pillar Writing
Write the full draft yourself (you are running on Claude Sonnet 5 already).
Requirements:
- Minimum 1500 words (1800+ preferred for pillar content)
- Built strictly from `core_facts` + `industry_terms` + SEO brief
- Concrete details: real named entities (ports, document types like EIR,
  Bill of Lading, ISF, BTI, etc. — whatever is actually relevant to the
  brief, do not force logistics vocabulary onto unrelated topics)
- No AI clichés: forbidden phrases include "end-to-end", "vital role",
  "in today's world", "delve into", and the full pattern list in the
  `humanizer` skill
- No em dashes (—) anywhere

### Stage 5: Humanizer & Stylist Pass
Apply the `humanizer` skill (load it with `skill_view(name='humanizer')` if
not already in context) plus the `avalanche-copywriting` skill rules:
- Break sentence rhythm: mix short (3-5 word) punches with longer explanatory
  sentences
- Add genuine editorial voice, practical asides, mild informality where the
  tone allows it
- Remove any remaining structural symmetry (identical paragraph shapes,
  mechanical bullet lists with bold headers)

### Stage 6: Link & Anchor Integration
Insert links to `www.navo24.com` and relevant authorities (WCO, ISO, IMO, or
whatever is topically correct) using markdown link syntax. Hard rule:
guaranteed whitespace before and after every hyperlink run so words never
glue together, e.g. `tools like [Navo24 Freight Portal](url) empower` — never
`tools like[Navo24 Freight Portal](url)empower`. Keep keyword density natural
(roughly 1-2%, do not force it).

### Stage 7: Adversarial Quality Gate (self-audit, no external API)
Switch mindset: review your own draft as a hostile, skeptical senior editor
looking for a reason to reject it. Check explicitly:
1. Does any sentence still read like a template or AI pattern? (cross-check
   against the `humanizer` pattern list)
2. Any em dash (—) present anywhere? Any Title Case headings? Any emoji?
3. Word count >= 1500 (or the requested minimum)?
4. Does the body actually match the stated topic/meta throughout, no drift?
5. Are all inserted links properly spaced (Stage 6 rule)?

Produce a small internal report:
```
{ "status": "PASS" | "FAIL", "issues": ["..."] }
```
This is an internal editorial judgment call, not a percentage AI-detection
score — never state a fabricated "% AI score" since no detector API is wired
up.

### Stage 8: Fix Loop
If `status == "FAIL"`, go back to Stage 5 with the specific issues listed,
rewrite the affected sections, then repeat Stage 7. Cap this at 3 total
audit passes. If still failing after 3 passes, proceed anyway but flag the
unresolved issues clearly in the delivery message — do not silently ship a
piece the audit rejected without saying so.

### Stage 9: DOCX Generation & Delivery
1. Load the `docx` skill and generate a clean `.docx`:
   - Proper H1/H2/H3 heading styles
   - No embedded images
   - Save to `/opt/hermes/profiles/archie/content_pipeline/output/<queue_id>_<slug>.docx`
2. Mark the queue item done:
   ```bash
   python3 /opt/hermes/profiles/archie/content_pipeline/queue_manager.py done <id> --output=<path>
   ```
3. Deliver the finished file to the user in Telegram (attach the docx path)
   along with a short delivery note: word count, audit pass/fail history,
   and any unresolved issues from Stage 8.

## Error handling

If any stage fails hard (extraction returns nothing usable, the source URL
is dead, etc.), do not silently drop the item:
```bash
python3 /opt/hermes/profiles/archie/content_pipeline/queue_manager.py fail <id> "<short reason>"
```
This automatically requeues it up to 3 attempts before marking it permanently
`failed`. Report the failure to the user briefly, do not let a cron tick
crash silently.

## Running it

**Manual trigger** (user says "прогони пайплайн" / "обработай очередь"):
just execute Step 0 onward yourself, right now, in this turn.

**Recurring cron** (the intended steady-state mode): a cron job calls this
skill on a schedule (e.g. every 45-60 minutes) with a prompt like "Run one
tick of the avalanche-content-pipeline skill." Each tick processes exactly
one queue item and exits — this keeps individual agent turns short and
avoids one giant multi-hour session. If the queue is empty, the tick does
nothing and delivers nothing (see Step 0).

## Adding items to the queue (for the user)

Tell the user they can add work by messaging Archie in Telegram, e.g.:
- "Добавь в очередь: https://searates.com/some-article" (rewrite existing article)
- "Добавь тему в очередь: Демередж и детеншн в морских контейнерных перевозках" (net-new topic)

Archie should recognize this intent and run the `add` command directly
rather than waiting for a cron tick.
