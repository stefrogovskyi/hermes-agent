# Hermes skill with linked references to LIVE files (key trick)

## Problem
A skill's SKILL.md lives in `~/AppData/Local/hermes/skills/<cat>/<name>/`.
If you COPY the project's big .md files there, the copies rot when the live
project edits them. The agent then reads stale persona/knowledge.

## Fix: point references at the live files
Under the skill, register `references/<file>.md` whose CONTENT is a one-line
pointer to the live project path — not a copy:

```
Symlink-style reference — read the LIVE project file, do not edit here:
C:\Users\...\Richard Hermes\soul.md
(Richard's personality: honesty over pitching, precision like the data spine...)
```

Register via:
`skill_manage(action='write_file', name='<skill>', file_path='references/soul.md', file_content='...')`

In SKILL.md, state the PROJECT FOLDER explicitly and tell the agent to read
from there:
"Read `memory.md` FIRST — live file at <project folder>\memory.md."

## Activation order
1. `memory.md` (live, curated) FIRST
2. `soul.md` + SKILL.md for persona/focus
3. other files (Agents.md, tools.md, config) as needed

## Gotcha
- The linked-reference file is a POINTER, not a mirror. Don't paste the full
  source into it — that defeats the purpose.
- If the skill was created manually (not via skill_manage create), the curator
  may flag it `created_by=None` and block autonomous patch/write_file on it.
  In that case, keep project-specific pointers in a SEPARATE class-level skill
  you DO own (e.g. agent-project-wiring), and leave the manual skill alone.