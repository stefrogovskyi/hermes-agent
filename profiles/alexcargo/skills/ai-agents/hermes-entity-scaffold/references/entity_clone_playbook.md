# Entity clone playbook — detail + verification recipe

Companion to the `hermes-entity-scaffold` skill. Concrete steps and a throwaway
verification script you can `write_file` to `%LOCALAPPDATA%\Temp\`, run, then delete.

## Source → target (the Liz Harper case)
- Source: `…\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes\`
- Target: `…\Enlight Group\Enlight Board\Liz Harper\Liz Harper Hermes\`
- Registry: `…\Stefan Rogovskyi\Hermes Stevenson\entities\registry.json` + `entities/liz_harper.md`

## Rebrand token table (bot runtime)
| find | replace |
|---|---|
| `r"@(qubicpmbot)\b"` | `r"@(lizharpbot)\b"` |
| `(алистер\|alistair\|allister\|alister)` | `(лиз\|элизабет\|елизавета\|liz\|harper\|elizabeth\|лиза\|lisa)` |
| `BOT_USERNAME = "qubicpmbot"` | `BOT_USERNAME = "lizharpbot"` |
| `ALISTAIR_MODEL` | `LIZ_MODEL` |
| `ALISTAIR_SYSTEM` | `LIZ_SYSTEM` |
| `ALISTAIR_STUB_MESSAGE` | `LIZ_STUB_MESSAGE` |
| `ALISTAIR_SELFTEST` | `LIZ_SELFTEST` |
| `"----alistairvoice"` | `"----lizvoice"` |
| `"----alistairboundary"` | `"----lizboundary"` |
| `"alistair.lock"` | `"liz.lock"` |
| `"alistair_memory.json"` | `"liz_memory.json"` |
| `[Alistair]` | `[Liz]` |
| fallback `"Alistair Sterling, AI project manager at Navo …"` | `"Elizabeth Harper, Chief People Officer at Enlight Group …"` |
| error phrase `"Alistair here — lost the line …"` | `"Liz here — lost the line …"` |
| `имя Алистера` | `имя Лиз` |

Keep comments like "скопирован 1:1 из бота Алистера" — they are true.

## Ad-hoc verification script (run then delete)
```python
# -*- coding: utf-8 -*-
import json, os, subprocess, sys, py_compile
BASE = r"C:\Users\Stefan\My Drive\Equity\My Biz\My companies\Enlight Group"
LIZ = os.path.join(BASE, r"Enlight Board\Liz Harper\Liz Harper Hermes")
REG = os.path.join(BASE, r"Stefan Rogovskyi\Hermes Stevenson\entities\registry.json")
res = []
def ck(n, ok, d=""):
    res.append(ok); print(("[PASS] " if ok else "[FAIL] ") + n + ((" — "+d) if d else ""))
reg = json.load(open(REG, encoding="utf-8"))
ids = [e["id"] for e in reg["entities"]]
ck("registry valid + liz_harper present", "liz_harper" in ids, "ids=%s" % ids)
ck("count==4", reg["meta"]["count"] == 4)
for fn in ["liz_harper_bot.py","tasktracker_client.py","liz_watchdog.py"]:
    try: py_compile.compile(os.path.join(LIZ, fn), doraise=True); ck("compile "+fn, True)
    except Exception as e: ck("compile "+fn, False, str(e))
env = dict(os.environ); env["LIZ_SELFTEST"] = "список задач"
out = subprocess.run([sys.executable, os.path.join(LIZ,"liz_harper_bot.py")],
                     capture_output=True, text=True, env=env, timeout=30, cwd=LIZ)
txt = (out.stdout or "") + (out.stderr or "")
ck("runtime selftest runs", bool(txt.strip()), txt.strip().splitlines()[0] if txt.strip() else "")
bot = open(os.path.join(LIZ,"liz_harper_bot.py"), encoding="utf-8").read()
ck("no qubicpmbot/ALISTAIR in bot", "qubicpmbot" not in bot and "ALISTAIR" not in bot)
ck("bot references lizharpbot + LIZ_SYSTEM", "lizharpbot" in bot and "LIZ_SYSTEM" in bot)
for fn in ["system_prompt.md","soul.md","Agents.md","memory.md","tools.md","agent.config.json"]:
    ck("exists "+fn, os.path.exists(os.path.join(LIZ, fn)))
p = sum(1 for r in res if r); print("\n=== %d/%d passed ===" % (p, len(res)))
sys.exit(0 if p == len(res) else 1)
```
Run `python <script>` then `rm` it. Re-run on demand for fresh evidence.

## Real-mode activation (not done by the scaffold)
- `TELEGRAM_BOT_TOKEN` for `@lizharpbot` (or reuse pattern via @BotFather).
- `NOUS_API_KEY` (+ `NOUS_BASE_URL`), `OPENAI_API_KEY` for STT/vision,
  `SALESLOOP_API_KEY`, `LIZ_ADMIN_IDS`, `STEFAN_CHAT_ID`.
- `TASKTRACKER_BACKEND` = `sheets`/`rest`/`stub` (stub works offline).
- For groups: BotFather → /setprivacy → Disable (so mentions are visible).
