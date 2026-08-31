# Reconstructing an agent FROM a Make.com blueprint export

Reverse of the usual build: the user already ran the agent as a Make.com scenario
and hands you the exported `*.blueprint.json`. Goal = reproduce ALL its prompts +
architecture 1:1 as a local stdlib entity (the Richard Marlowe / Alistair Sterling
file set), then wire channels. Proven on the "Alistair Sterling Telegram" blueprint.

## Step 0 — intake & safety
- A blueprint export is huge (Make bloats it: module coords, metadata, repeats).
  Real logic is ~5-10%. The "Alistair" one was **1.47 MB / 366k tokens**.
- **Dropping the raw file into chat overflows context** — Hermes refused with
  `context injection refused: 366093 tokens exceeds the 50% hard limit (131072)`.
  Never paste the blueprint; put it in a folder and read it with tools.
- Users often bundle a **keys .txt** next to the blueprint. Treat any key that
  touched chat / an open file as COMPROMISED; advise re-issue. Redact when echoing:
  `sed -E 's/[A-Za-z0-9_-]{20,}/<REDACTED>/g'`. Keys go to `.env.local` only.

## Step 1 — parse the flow with Python (not jq; jq usually absent on Windows)
```python
import json
d=json.load(open(path,encoding='utf-8'))
flow=d['flow']                       # top-level module list
# module inventory:
from collections import Counter
c=Counter()
def rec(items):
    for m in items:
        c[m['module']]+=1
        for r in (m.get('routes') or []): rec(r.get('flow',[]))
rec(flow); print(c.most_common())
```
Module types map straight to capabilities:
- `telegram:WatchUpdates` = trigger; `telegram:SendReplyMessage` = outbound
- `groq:*` / `openai-gpt-3:createModelResponse` = LLM steps (prompts live in
  `mapper.messages[].content` or `mapper.input`)
- `builtin:BasicRouter` = branch; each downstream module carries its own `filter`
  (the routing condition) — routers themselves show no filter
- `google-sheets:*` = the data store (CRUD); `google-docs:getADocument` = JD/context
- `openai-gpt-3:CreateTranslation` (whisper) = voice; `analyzeImages` = vision
- `datastore:*` = conversation memory; `http:MakeRequest` = external API;
  `make:runScenarioWithInputs` = a sub-scenario (note the id, reproduce separately)

## Step 2 — dump prompts + params to a FILE, then read it
The extracted logic is small (~32 KB for Alistair) even though the source is 1.5 MB.
Walk the tree, write each node's `module`, designer name, `filter`, and for LLM
nodes the full `messages`/`input`/`model`, for others a compact `mapper`, to a
`_extracted_logic.txt`. THEN `read_file` that — it fits context; the raw never will.
Preserve prompts **verbatim** (they are the persona) — do not paraphrase.

## Step 3 — map to the entity file set
- Prompts → `system_prompt.md` (verbatim rules: date format, default timeline,
  owner-from-Team, "no data" honesty, language-matches-question, command grammar).
- Flow/branches/filters/data model → `Agents.md` (commands table, sheet columns,
  trigger conditions from the "Initial filters" block, integrations w/ IDs).
- Each external module → a tool in a stdlib client (`<agent>_client.py`) exposing
  the same operations (e.g. add/update/delete/list/status) with `stub|rest|sheets`
  backends so it runs BEFORE real creds exist. Default `stub` = local JSON file.
- Runtime `<agent>_bot.py` — copy the proven Richard bot (long-poll, PID-lock,
  tiered memory, Whisper/vision, stub-mode) and swap persona + tool client.

## Step 4 — verify in stub mode, register, GitHub
- CRUD round-trip via the client CLI; `ast.parse` both .py; JSON config valid;
  selftest env (`<AGENT>_SELFTEST=...`) returns the honest stub string with no keys.
- Register in orchestrator `entities/registry.json` + `entities/<id>.md`, bump
  `meta.count`/`active`.
- `git init` → confirm `git status --short` shows NO `.env.local`, keys .txt,
  `*.blueprint.json`, or `_extracted_logic.txt` (add them to `.gitignore`), commit,
  `gh repo create <slug> --private --source=. --push`, then leak-check:
  `gh api repos/<owner>/<slug>/contents --jq '.[].name' | grep -Ei 'env|key|blueprint'`
  must be empty.

## Pitfall — large file writes time out; chunk them
Writing a ~700-line bot via `write_file` in one shot **stalled the stream mid-call**
("stream stalled / too large … under ~8K tokens"). Fix: write the header with
`write_file`, then append the remaining logical blocks with
`cat >> file <<'PYEOF' … PYEOF` in separate `terminal` calls (each < ~8K tokens),
and finish with `python -c "import ast; ast.parse(open('f').read())"`. Same limit
hit `skill_manage` — split skill edits into small patches too.

## Pitfall — MSYS mktemp path invisible to Windows python
`mktemp` in git-bash returns `/c/tmp/..` (really `C:\tmp\..`) which the Windows
`python.exe` can't open. Put verify scripts under `"$LOCALAPPDATA\Temp\hermes-verify-*.py"`
instead. Note a temp script isn't on `sys.path`, so `import <client>` from it fails —
either `cd` to the agent folder and run there, or `sys.path.insert(0,'.')`.
