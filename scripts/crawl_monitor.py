#!/usr/bin/env python3
# crawl_monitor.py — докладывает прогресс краулинга shippingchina (расширение).
# Формат Стефана: время / текущая строка / прогресс % / время остается.
# v2: без фиксированного EST_TOTAL (лимиты сняты — идём до конца каталога),
#     прогресс считается по страницам, скорость по дельте страниц,
#     плюс проверка что процесс extend_subs.py реально жив.
import os, json, subprocess
from datetime import datetime

DETAILS = r"C:\Users\Stefan\scrape_sc\details.jsonl"
NEW_SUBS = r"C:\Users\Stefan\scrape_sc\new_subs.json"
EXT_STATE = r"C:\Users\Stefan\scrape_sc\extend_state.json"
STATE = r"C:\Users\Stefan\AppData\Local\hermes\scripts\.crawl_monitor_state"
SEED = 3001
NOWIN = 0x08000000


def crawler_alive():
    try:
        out = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
             "Where-Object { $_.CommandLine -match 'extend_subs' } | "
             "Select-Object -ExpandProperty ProcessId"],
            capture_output=True, text=True, timeout=60, creationflags=NOWIN).stdout.strip()
        return out.splitlines()[0] if out else None
    except Exception:
        return None


def main():
    now = datetime.now()
    # готовые детали
    n_det = 0
    if os.path.exists(DETAILS):
        with open(DETAILS, "r", encoding="utf-8", errors="ignore") as f:
            for _ in f:
                n_det += 1
    # новые subdomain (найдены, деталей ещё нет)
    n_new = 0
    if os.path.exists(NEW_SUBS):
        try:
            n_new = len(json.load(open(NEW_SUBS, encoding="utf-8")))
        except Exception:
            n_new = 0
    # текущая страница
    page = 0
    if os.path.exists(EXT_STATE):
        try:
            st = json.load(open(EXT_STATE, encoding="utf-8"))
            page = int(st.get("cargo_page", 0))
        except Exception:
            page = 0
    total_found = SEED + n_new

    # state (для скорости: дельта страниц и находок)
    prev = {}
    if os.path.exists(STATE):
        try:
            l = json.load(open(STATE, "r", encoding="utf-8"))
            if isinstance(l, dict):
                prev = l
        except Exception:
            pass
    try:
        json.dump({"found": total_found, "page": page, "ts": now.timestamp()},
                  open(STATE, "w", encoding="utf-8"))
    except Exception:
        pass

    pages_per_min = 0.0
    finds_per_min = 0.0
    if prev.get("ts"):
        dt = (now.timestamp() - prev["ts"]) / 60.0
        if dt > 0:
            pages_per_min = max(0.0, (page - prev.get("page", page)) / dt)
            finds_per_min = max(0.0, (total_found - prev.get("found", total_found)) / dt)

    pid = crawler_alive()

    print(f"время: {now.strftime('%H:%M')}")
    print(f"страница обхода: cargo #{page} (лимит снят — идём до конца каталога)")
    print(f"найдено уникальных: {total_found} (+{n_new} новых с начала расширения)")
    print(f"детали собраны: {n_det}")
    if pages_per_min > 0:
        print(f"скорость: ~{pages_per_min:.1f} стр/мин, ~{finds_per_min:.0f} новых/мин")
    if pid:
        print(f"процесс: жив (PID {pid})")
    else:
        print("⚠️ процесс extend_subs.py НЕ ЗАПУЩЕН — краулер стоит!")
    if prev.get("page") is not None and page <= prev.get("page", 0) and pid:
        pt = datetime.fromtimestamp(prev["ts"]).strftime("%H:%M") if prev.get("ts") else "?"
        print(f"⚠️ страница не растёт с {pt} — возможно процесс завис")


if __name__ == "__main__":
    main()
