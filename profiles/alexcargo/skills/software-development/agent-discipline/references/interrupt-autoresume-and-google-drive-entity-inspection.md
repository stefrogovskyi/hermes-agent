# Interrupt Auto-Resume & Google Drive Entity Inspection

## 1. Interrupt Auto-Resume Protocol
When Hermes detects an interruption (`[This response was interrupted by a user correction.]`, SSE gateway timeout, or restart):
1. **Never ask "Что делать дальше?" or "How should we proceed?".**
2. Immediately reconstruct the active task goal from the preceding messages and tool state.
3. Log the failure/interruption internally.
4. Automatically continue execution from the exact checkpoint where the interruption occurred.

## 2. Fact-First Entity Inspection (Google Drive Sync)
Virtual employees and AI agents (Richard, Liz, Alistair, Ben) have their live identity files stored on Google Drive at `C:\Users\Stefan\My Drive\...`.
- **Rule:** Never answer identity, JD, role, or configuration questions about an agent from memory alone.
- **Action:** Read the live `soul.md`, `system_prompt.md`, `AGENTS.md`, or `agent.config.json` directly from their respective Google Drive folder before answering.
- **Directory map:**
  - Liz Harper (`@lizharperbot`): `C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Enlight Board\Liz Harper\Liz Harper Hermes`
  - Richard Marlowe (`@richnavobot`): `C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Richard Marlowe\Richard Hermes`
  - Alistair Sterling (`@qubicpmbot`): `C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes`
  - Ben Jett (`@benjettbot`): `C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group\Avalanche Agency\Team\Ben Jett\Ben Jett Hermes`
