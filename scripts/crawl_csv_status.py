# -*- coding: utf-8 -*-
"""Статус сборки details.jsonl -> CSV (китайские экспедиторы shippingchina)."""
import os, json, time

WORK = r"C:\Users\Stefan\scrape_sc"
jsonl = os.path.join(WORK, "details.jsonl")
log = os.path.join(WORK, "details_new.log")
new_subs = os.path.join(WORK, "new_subs.json")

# сколько субдоменов в работе
try:
    total = len(json.load(open(new_subs, encoding="utf-8")))
except Exception:
    total = "?"

# сколько записей деталей собрано
done = 0
err = 0
if os.path.exists(jsonl):
    with open(jsonl, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            done += 1
            try:
                if json.loads(line).get("error"):
                    err += 1
            except Exception:
                pass

pct = (done / total * 100) if isinstance(total, int) and total else 0

# процесс жив?
import subprocess
alive = False
try:
    out = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
         "Where-Object { $_.CommandLine -match 'details_new' }).Count"],
        capture_output=True, text=True, timeout=30,
        creationflags=0x08000000).stdout
    alive = out.strip() not in ("", "0")
except Exception:
    pass

# последний лог-маркер
last = ""
if os.path.exists(log):
    with open(log, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                last = line
    last = last[-120:]

csv_ready = os.path.exists(os.path.join(WORK, "cn_forwarders_all.csv"))

status = "🟢 идёт" if alive else ("✅ CSV готов" if csv_ready else "⚪️ процесс не найден")
print(f"📊 Статус сбора деталей (shippingchina)\n"
      f"Процесс: {status}\n"
      f"Собрано записей: {done:,} / {total:,} ({pct:.1f}%)\n"
      f"  └ ошибок fetch: {err:,}\n"
      f"Осталось: {(total-done) if isinstance(total,int) else '?':,}\n"
      f"Последний маркер: {last}")
if csv_ready:
    print("✅ CSV уже сформирован — уведомления можно отключить.")
