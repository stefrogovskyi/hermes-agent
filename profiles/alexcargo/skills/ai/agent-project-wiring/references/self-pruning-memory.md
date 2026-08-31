# Self-pruning agent memory (keep the agent light)

## Why
An agent that hoards every fact gets slow and noisy. A curated `memory.md`,
rewritten weekly by a cron "steward", keeps high-signal facts and drops
stale ones. Forgetting dead facts is GOOD.

## Shape (used by richard-marlowe)
- `memory.md` in the project folder = the agent's live, curated working memory.
- On every skill activation, read `memory.md` FIRST (before soul/persona),
  so the agent "loads itself" automatically.
- Declared in `agent.config.json`:
  ```json
  "memory": { "type":"file", "path":"memory.md",
    "auto_load_on_activation": true,
    "self_inventory": { "schedule":"weekly", "target_max_lines":150,
      "keep":"high-signal, currently-relevant", "drop":"stale one-off / outdated / never-recur" } }
  ```

## The weekly steward cron
`cronjob(action='create', schedule='0 3 * * 0', prompt=...)` where the
prompt: read memory.md (+ soul.md/Agents.md for context), DROP stale/outdated/
duplicate/never-recur items, KEEP active client relationships, changed competitive
intel, daily-cited product facts, recurring gotchas, and the pruning-rules block
itself. Rewrite memory.md full-replacement, preserve header + pruning-rules
section. Target < ~150 lines. Output a short kept/dropped report.

## Gotcha
- Deliver mode: a CLI/TUI cron has no live-delivery channel — set
  `deliver='local'` (saved, viewable) or `deliver='telegram'` if a gateway
  is connected. The default "local" still RUNS the job; you just won't get
  a chat ping unless you set a delivery target.
- Don't let the steward delete the "Pruning rules" section — it needs it next week.