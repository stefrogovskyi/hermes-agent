# -*- coding: utf-8 -*-
"""
add_dpworld_cron_to_alistair.py — Настройка ежедневной крон-задачи вакансий DP World у Алистера (09:00 MSK):
  - Скрипт: C:\\Users\\Stefan\\AppData\\Local\\hermes\\scripts\\check_dpworld_jobs.py
  - Доставка: напряму от Алистера (@qubicpmbot)
"""

import os, json, time

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
alistair_cron_dir = os.path.join(HERMES_DIR, "profiles", "alistair", "cron")
os.makedirs(alistair_cron_dir, exist_ok=True)

jobs_p = os.path.join(alistair_cron_dir, "jobs.json")

jobs = {}
if os.path.exists(jobs_p):
    try:
        jobs = json.load(open(jobs_p, encoding="utf-8"))
    except Exception:
        jobs = {}

dpworld_job = {
    "job_id": "dpworld_daily_vacancies",
    "name": "DP World Daily Vacancies Poller",
    "schedule": "0 9 * * *",
    "script": r"C:\Users\Stefan\AppData\Local\hermes\scripts\check_dpworld_jobs.py",
    "deliver": "origin",
    "created_at": time.time(),
    "last_run_at": time.time()
}

jobs["dpworld_daily_vacancies"] = dpworld_job

open(jobs_p, "w", encoding="utf-8").write(json.dumps(jobs, indent=2, ensure_ascii=False))
print("✅ Successfully configured DP World daily vacancies cron job for Alistair (@qubicpmbot)!")
