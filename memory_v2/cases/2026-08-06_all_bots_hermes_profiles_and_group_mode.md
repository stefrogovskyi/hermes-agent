# Case: Sub-Bots Hermes Profile Migration, Group Mention Policy & System Reorganization

## Symptom
1. Sub-bots (Richard, Liz, Alistair, Ben, Callum) were running on custom legacy scripts with duplicated LLM fallback logic, causing occasional polling stalls, high CPU spikes, and zombie python processes.
2. Bots in Telegram groups were answering unprompted or generating meta-commentary when not tagged.
3. Folder structures on Desktop/Drive had duplicate locations (e.g. `Orchestrator Hermes` moved by Stefan, `Google AI Studio` folder duplication).

## Hypothesis vs Fact
- **Hypothesis**: The bots needed individual custom watchdog scripts and separate gateway instances.
- **Fact**: Converting sub-bots into isolated native Hermes profiles under `AppData/Local/hermes/profiles/<name>/` unifies toolsets, fallbacks, memory, and gateway lifecycle management under Hermes standard architecture.

## Root Cause
- Sub-bots grew as individual python scripts outside the main Hermes profile framework.
- Group response settings were not explicitly enforced across all 5 bot system prompts and gateway routing rules.

## Fix
1. Converted/created Hermes profiles for all 5 sub-bots (`profiles/richard/`, `profiles/liz/`, `profiles/alistair/`, `profiles/ben/`, `profiles/callum/`).
2. Configured Callum Vance (`@callumvancebot`) as 5th domain agent (Full-Stack Tech Lead helper).
3. Enforced strict `@mention` group chat response mode across all 5 bot profiles (`set_group_response_mode_mention_all_bots.py`).
4. System process audit: terminated zombie/duplicate python processes and configured clean watchdog launchers.
5. Reorganized folders: relocated `Orchestrator Hermes` to `C:\Users\Stefan\Documents\Stefan25\5. Soft\1. AI soft\Hermes\Orchestrator Hermes`, merged `Google AI Studio` and `Google AI Studio (1)` folders on Drive, and sorted Downloads voice memos into `Voice_Memos/`.

## Key Lesson / Principle
Sub-agents must be managed as first-class persistent Hermes profiles rather than ad-hoc custom scripts. Group response policies must be explicitly configured in both gateway routing and system prompts.
