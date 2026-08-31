# Self-Recovery Protocol (Stefan, 2026-07-28 — verbatim directive)

"При любом падении независимо от причины - возобновляй работу самостоятельно,
в первую очередь доделываешь задачу, затем анализируешь причину падения и
исправляешь ее. Например если state.db это память сессии - то сам начинай новую
сессию. Если 3 итерации подряд не выходит продолжить задачу или закончить ее -
сразу переходишь к анализу и исправлению причины падения."

## Operational translation
1. Failure happens (any cause: disk, DB lock, API 5xx, crash) → DON'T wait for
   Stefan. Auto-resume.
2. Priority order: (a) FINISH the current task, (b) then analyze why it failed,
   (c) then fix the root cause.
3. Concrete mapping:
   - state.db write error / "session storage could not be written" → start a fresh
     session; the heavy transcript is preserved in state.db, just begin anew.
   - Process died → restart it (background + notify), don't ask.
   - 3 consecutive failed iterations on the SAME task → STOP retrying, switch to
     root-cause analysis + fix of the failure itself.
4. Report the failure + recovery to Stefan proactively afterward (proactivity rule).

## Why
Silence >10 min on a broken process is unacceptable to Stefan. Self-healing keeps
the agent fleet running without human babysitting.
