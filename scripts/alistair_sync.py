#!/usr/bin/env python3
"""alistair_sync.py — ежедневный авто-синк канбана Гаффера в Google Таблицу.

Запускается по крону (раз в день в 7:00). Вызывает sync_to_sheets() из
tasktracker_client.py Алистера: канбан Гаффера -> вкладка Tracker, строго
по инструкции Стефана (не трогает чужие строки, матч по ID, дописывает
после основного блока). stdout идёт в отчёт крона.
"""
import os
import sys
import importlib.util

AH = r"C:\Users\Stefan\My Drive\Equity\My Biz\Partner companies\Navo\6. Departments\Alister Sterling\Alistair Hermes"


def main():
    # загружаем .env.local
    for envf in (".env", ".env.local"):
        p = os.path.join(AH, envf)
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ[k.strip()] = v.strip().strip('"').strip("'")

    # импортируем модуль Алистера
    spec = importlib.util.spec_from_file_location(
        "tasktracker_client", os.path.join(AH, "tasktracker_client.py"))
    tt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tt)

    res = tt.sync_to_sheets()
    print("Alistair sync:", res)


if __name__ == "__main__":
    main()
