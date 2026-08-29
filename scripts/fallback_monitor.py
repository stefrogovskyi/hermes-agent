#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fallback_monitor.py — Кроссплатформенный (Linux/Windows) аудит fallback-цепочки, пинг моделей и синхронизация во вкладку 'Models' в Google Таблицу.
"""

import os, sys, json, time, requests, yaml, urllib.request, urllib.parse
from datetime import datetime, timezone, timedelta
from concurrent.futures import ThreadPoolExecutor

# Force UTF-8 on Windows console / stdout
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Cross-platform HERMES_HOME detection
if os.name == "nt":
    DEFAULT_HOME = os.path.expandvars(r"%LOCALAPPDATA%\hermes")
    if not os.path.exists(DEFAULT_HOME):
        DEFAULT_HOME = os.path.join(os.path.expanduser("~"), "AppData", "Local", "hermes")
else:
    DEFAULT_HOME = "/opt/hermes"

HERMES_HOME = os.environ.get("HERMES_HOME", DEFAULT_HOME)
CONFIG_PATH = os.path.join(HERMES_HOME, "config.yaml")
AUTH_PATH = os.path.join(HERMES_HOME, "auth.json")
SHEET_CONFIG = os.path.join(HERMES_HOME, "ecosystem_registry_sheet.json")
GOOGLE_TOKEN_PATH = os.path.join(HERMES_HOME, "profiles", "archie", "google_token.json")
GOOGLE_SECRET_PATH = os.path.join(HERMES_HOME, "profiles", "archie", "google_client_secret.json")

# Load environment keys from .env
env_file = os.path.join(HERMES_HOME, ".env")
keys = {}
if os.path.exists(env_file):
    with open(env_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                keys[k] = v

def get_nous_token():
    if os.path.exists(AUTH_PATH):
        try:
            with open(AUTH_PATH, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)
                return data.get("providers", {}).get("nous", {}).get("access_token")
        except Exception:
            pass
    return None

def get_claude_pro_cookie():
    path = os.path.join(os.path.expanduser("~"), ".claude", ".credentials.json")
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                data = json.load(f)
                oauth = data.get("claudeAiOauth", {})
                return oauth.get("accessToken")
        except Exception:
            pass
    return None

def ping_model(model_entry):
    model = model_entry["model"]
    provider = model_entry["provider"]
    nous_tok = get_nous_token()
    claude_tok = get_claude_pro_cookie()
    t0 = time.time()

    try:
        if provider == "openai":
            api_key = keys.get("OPENAI_API_KEY")
            if not api_key:
                return model, provider, "SKIPPED", "No OPENAI_API_KEY", 0
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
            r = requests.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers, timeout=10)
            latency = round(time.time() - t0, 2)
            if r.status_code == 200:
                return model, provider, "LIVE", f"{latency}s", latency
            else:
                return model, provider, f"ERR {r.status_code}", r.text[:80].replace("\n", " "), latency

        elif provider == "anthropic":
            tok = claude_tok or keys.get("ANTHROPIC_API_KEY")
            if not tok:
                return model, provider, "SKIPPED", "No ANTHROPIC Token/Key", 0
            
            headers = {"content-type": "application/json", "anthropic-version": "2023-06-01"}
            if claude_tok:
                headers["Authorization"] = f"Bearer {tok}"
                headers["anthropic-beta"] = "oauth-2025-04-20"
            else:
                headers["x-api-key"] = tok

            payload = {"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
            r = requests.post("https://api.anthropic.com/v1/messages", json=payload, headers=headers, timeout=10)
            latency = round(time.time() - t0, 2)
            if r.status_code == 200:
                return model, provider, "LIVE", f"{latency}s", latency
            elif r.status_code == 429:
                return model, provider, "LIVE (Auth OK)", "Rate limit / Pro sub active", latency
            else:
                return model, provider, f"ERR {r.status_code}", r.text[:80].replace("\n", " "), latency

        elif provider == "google":
            api_key = keys.get("GEMINI_API_KEY") or keys.get("GOOGLE_API_KEY")
            if not api_key:
                return model, provider, "SKIPPED", "No GOOGLE_API_KEY", 0
            m_clean = model.replace("google/", "")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{m_clean}:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": "ping"}]}], "generationConfig": {"maxOutputTokens": 5}}
            r = requests.post(url, json=payload, timeout=10)
            latency = round(time.time() - t0, 2)
            if r.status_code == 200:
                return model, provider, "LIVE", f"{latency}s", latency
            else:
                return model, provider, f"ERR {r.status_code}", r.text[:80].replace("\n", " "), latency

        elif provider == "huggingface":
            api_key = keys.get("HF_TOKEN")
            if not api_key:
                return model, provider, "SKIPPED", "No HF_TOKEN", 0
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
            r = requests.post("https://router.huggingface.co/v1/chat/completions", json=payload, headers=headers, timeout=10)
            latency = round(time.time() - t0, 2)
            if r.status_code == 200:
                return model, provider, "LIVE", f"{latency}s", latency
            else:
                return model, provider, f"ERR {r.status_code}", r.text[:80].replace("\n", " "), latency

        elif provider == "nous":
            tok = nous_tok or keys.get("NOUS_API_KEY")
            if not tok:
                return model, provider, "SKIPPED", "No Nous Token", 0
            headers = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}
            payload = {"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
            r = requests.post("https://inference-api.nousresearch.com/v1/chat/completions", json=payload, headers=headers, timeout=10)
            latency = round(time.time() - t0, 2)
            if r.status_code == 200:
                return model, provider, "LIVE", f"{latency}s", latency
            elif r.status_code == 429:
                return model, provider, "BUSY (429)", "Rate limit / capacity", latency
            else:
                return model, provider, f"ERR {r.status_code}", r.text[:80].replace("\n", " "), latency

        elif provider == "openrouter":
            api_key = keys.get("OPENROUTER_API_KEY")
            if not api_key:
                return model, provider, "SKIPPED", "No OPENROUTER_API_KEY", 0
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
            r = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=10)
            latency = round(time.time() - t0, 2)
            if r.status_code == 200:
                return model, provider, "LIVE", f"{latency}s", latency
            elif r.status_code == 429:
                return model, provider, "BUSY (429)", "Rate limit", latency
            else:
                return model, provider, f"ERR {r.status_code}", r.text[:80].replace("\n", " "), latency

        elif provider == "gonka24":
            api_key = keys.get("GONKA24_API_KEY")
            if not api_key:
                return model, provider, "SKIPPED", "No GONKA24_API_KEY", 0
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {"model": model, "messages": [{"role": "user", "content": "ping"}], "max_tokens": 5}
            r = requests.post("https://api.gonka24.com/v1/chat/completions", json=payload, headers=headers, timeout=10)
            latency = round(time.time() - t0, 2)
            if r.status_code == 200:
                return model, provider, "LIVE", f"{latency}s", latency
            else:
                return model, provider, f"ERR {r.status_code}", r.text[:80].replace("\n", " "), latency

        else:
            return model, provider, "UNSUPPORTED", "Unknown provider", 0

    except Exception as e:
        latency = round(time.time() - t0, 2)
        return model, provider, "TIMEOUT/EXC", str(e)[:60], latency

def classify_tier(model_name, provider):
    m = model_name.lower()
    # Tier 3: Heavy Reasoning & Deep Architecture
    if any(k in m for k in ["r1", "opus", "sonnet", "fable", "405b", "70b", "72b", "120b", "550b", "2.5-pro", "deepseek-v3", "deepseek-chat"]):
        return 3
    if m == "gpt-4o":
        return 3
    # Tier 2: Standard Workhorse
    if any(k in m for k in ["3.7-flash", "3.6-flash", "coder", "small-24b", "m2.7", "k2.6", "gemma-4", "m3:free", "glm-5.2", "openrouter/free"]):
        return 2
    # Tier 1: Light & Free Tier
    return 1

def sync_to_google_sheet(results, kyiv_timestamp):
    if not os.path.exists(GOOGLE_TOKEN_PATH) or not os.path.exists(SHEET_CONFIG):
        return False

    with open(GOOGLE_TOKEN_PATH, "r", encoding="utf-8", errors="ignore") as f:
        token_data = json.load(f)
    with open(SHEET_CONFIG, "r", encoding="utf-8", errors="ignore") as f:
        sheet_info = json.load(f)

    spreadsheet_id = sheet_info.get("spreadsheet_id")
    access_token = token_data.get("access_token")
    refresh_token = token_data.get("refresh_token")

    if refresh_token and os.path.exists(GOOGLE_SECRET_PATH):
        try:
            with open(GOOGLE_SECRET_PATH, "r", encoding="utf-8", errors="ignore") as f:
                cs = json.load(f)
                client_info = cs.get("installed") or cs.get("web") or {}
                client_id = client_info.get("client_id")
                client_secret = client_info.get("client_secret")
            if client_id and client_secret:
                url = "https://oauth2.googleapis.com/token"
                data = urllib.parse.urlencode({
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "refresh_token": refresh_token,
                    "grant_type": "refresh_token"
                }).encode()
                req = urllib.request.Request(url, data=data)
                with urllib.request.urlopen(req) as resp:
                    new_token_data = json.loads(resp.read().decode())
                    access_token = new_token_data["access_token"]
                    token_data["access_token"] = access_token
                    with open(GOOGLE_TOKEN_PATH, "w", encoding="utf-8") as f_out:
                        json.dump(token_data, f_out)
        except Exception:
            pass

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

    rows = [
        [f"🕒 Последнее обновление: {kyiv_timestamp}", "", "", "", "", ""],
        ["Провайдер", "Модель", "Тир (Назначение)", "Статус", "Пинг (сек)", "Детали / Примечание"]
    ]

    tier_names = {
        3: "Tier 3 (Reasoning & Deep Arch)",
        2: "Tier 2 (Standard Workhorse)",
        1: "Tier 1 (Fast & Free / Light)"
    }

    # Sort results by Tier desc (3 -> 2 -> 1), then LIVE status
    sorted_results = sorted(results, key=lambda x: (classify_tier(x[0], x[1]), "LIVE" in x[2]), reverse=True)

    for model, provider, status, detail, latency in sorted_results:
        t = classify_tier(model, provider)
        t_label = tier_names.get(t, f"Tier {t}")
        status_clean = "✅ LIVE" if "LIVE" in status else ("⏳ BUSY (429)" if "BUSY" in status or "429" in status else f"⚠️ {status}")
        rows.append([
            provider.upper(),
            model,
            t_label,
            status_clean,
            f"{latency}s" if latency > 0 else "-",
            detail
        ])

    range_clear = urllib.parse.quote("Models!A1:F200")
    clear_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{range_clear}:clear"
    try:
        req_clear = urllib.request.Request(clear_url, data=b"{}", headers=headers, method="POST")
        urllib.request.urlopen(req_clear)
    except Exception:
        pass

    range_name = f"Models!A1:F{len(rows)}"
    encoded_range = urllib.parse.quote(range_name)
    update_url = f"https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{encoded_range}?valueInputOption=RAW"
    body = {"range": range_name, "majorDimension": "ROWS", "values": rows}

    try:
        req_up = urllib.request.Request(update_url, data=json.dumps(body).encode(), headers=headers, method="PUT")
        with urllib.request.urlopen(req_up) as resp:
            return True
    except Exception as e:
        print(f"Sheet update error: {e}")
        return False

def main():
    kyiv_time = datetime.now(timezone(timedelta(hours=3))).strftime("%Y-%m-%d %H:%M:%S (Киев)")

    if not os.path.exists(CONFIG_PATH):
        print(f"Error: Config not found at {CONFIG_PATH}")
        return

    with open(CONFIG_PATH, "r", encoding="utf-8", errors="ignore") as f:
        cfg = yaml.safe_load(f) or {}

    current_fallback = cfg.get("fallback", [])
    if not current_fallback:
        current_fallback = cfg.get("fallback_providers", [])

    # 1. Health-check current fallback models
    results = []
    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = [ex.submit(ping_model, m) for m in current_fallback]
        for f in futures:
            results.append(f.result())

    # Map results
    active_fallback = []
    pruned_models = []
    table_rows = []

    for (model, provider, status, detail, latency), original_entry in zip(results, current_fallback):
        if "404" in status or "does not exist" in detail.lower() or "not found" in detail.lower():
            pruned_models.append((model, provider, detail))
        else:
            active_fallback.append(original_entry)

        status_emoji = "✅" if "LIVE" in status else ("⏳" if "429" in status or "BUSY" in status else "⚠️")
        table_rows.append(f"{status_emoji} `{model}` ({provider}) — **{status}** ({detail})")

    # 2. Discovery: Scan OpenRouter for new free models
    new_discovered = []
    try:
        r_or = requests.get("https://openrouter.ai/api/v1/models", timeout=8)
        if r_or.status_code == 200:
            existing_model_names = {m["model"] for m in active_fallback}
            for m in r_or.json().get("data", []):
                mid = m.get("id", "")
                pricing = m.get("pricing", {})
                is_free = (str(pricing.get("prompt")) == "0" and str(pricing.get("completion")) == "0") or ":free" in mid
                if is_free and mid not in existing_model_names:
                    if not any(x in mid.lower() for x in ["safety", "embed", "vl", "audio", "lyria"]):
                        res = ping_model({"model": mid, "provider": "openrouter"})
                        if "LIVE" in res[2] or "BUSY" in res[2]:
                            entry = {"model": mid, "provider": "openrouter"}
                            active_fallback.append(entry)
                            existing_model_names.add(mid)
                            new_discovered.append((mid, "openrouter"))
                            results.append(res)
    except Exception:
        pass

    # 3. Discovery: Scan Nous Portal for new free models
    try:
        tok = get_nous_token() or keys.get("NOUS_API_KEY")
        if tok:
            r_nous = requests.get("https://inference-api.nousresearch.com/v1/models", headers={"Authorization": f"Bearer {tok}"}, timeout=8)
            if r_nous.status_code == 200:
                existing_model_names = {m["model"] for m in active_fallback}
                for m in r_nous.json().get("data", []):
                    mid = m.get("id", "")
                    if ":free" in mid and mid not in existing_model_names:
                        res = ping_model({"model": mid, "provider": "nous"})
                        if "LIVE" in res[2] or "BUSY" in res[2]:
                            entry = {"model": mid, "provider": "nous"}
                            active_fallback.append(entry)
                            existing_model_names.add(mid)
                            new_discovered.append((mid, "nous"))
                            results.append(res)
    except Exception:
        pass

    # 4. Sync full pool to Google Sheet 'Models' tab
    synced = sync_to_google_sheet(results, kyiv_time)

    # 5. Group active models by 3 Dynamic Tiers
    tier1_models = []
    tier2_models = []
    tier3_models = []

    for entry in active_fallback:
        t = classify_tier(entry["model"], entry["provider"])
        if t == 3:
            tier3_models.append(entry)
        elif t == 2:
            tier2_models.append(entry)
        else:
            tier1_models.append(entry)

    # 6. Build user digest
    report = []
    report.append(f"📊 **Ежедневный отчет Fallback-цепочки и пула моделей**")
    report.append(f"🕒 Время проверки: `{kyiv_time}`")
    report.append(f"🔢 Всего активных моделей в пуле: **{len(active_fallback)}**")
    if synced:
        report.append(f"✅ Вкладка **Models** в Google Sheet синхронизирована (всего моделей: **{len(results)}**)\n")

    if new_discovered:
        report.append("✨ **Новые обнаруженные и подключенные модели:**")
        for nm, np in new_discovered:
            report.append(f"- ➕ `{nm}` ({np})")
        report.append("")

    if pruned_models:
        report.append("🗑️ **Устаревшие/удаленные модели:**")
        for pm, pp, pd in pruned_models:
            report.append(f"- ❌ `{pm}` ({pp}) — {pd}")
        report.append("")

    report.append("🧠 **Конфигурация 3 Тиров Dynamic Model Routing:**\n")
    
    report.append(f"🔴 **Tier 3: Heavy Reasoning & Deep Architecture ({len(tier3_models)} моделей)**")
    report.append("*Назначение: системная архитектура, сложный кодинг, глубокий аудит, R1 рассуждения.*")
    for m in tier3_models[:10]:
        report.append(f"  • `{m['model']}` ({m['provider']})")
    if len(tier3_models) > 10:
        report.append(f"  • *...и еще {len(tier3_models) - 10} моделей*")
    report.append("")

    report.append(f"🟡 **Tier 2: Standard Workhorse ({len(tier2_models)} моделей)**")
    report.append("*Назначение: стандартная разработка, поиск, документы, сводки (дефолт).*\n")
    for m in tier2_models[:10]:
        report.append(f"  • `{m['model']}` ({m['provider']})\n")
    if len(tier2_models) > 10:
        report.append(f"  • *...и еще {len(tier2_models) - 10} моделей*\n")

    report.append(f"🟢 **Tier 1: Light & Free Tier ({len(tier1_models)} моделей)**")
    report.append("*Назначение: повседневный диалог, шутки, приветствия, быстрые статусы (<1s).*\n")
    for m in tier1_models[:10]:
        report.append(f"  • `{m['model']}` ({m['provider']})\n")
    if len(tier1_models) > 10:
        report.append(f"  • *...и еще {len(tier1_models) - 10} моделей*\n")

    report.append("📋 **Текущий статус цепочки резервирования (Health-Check):**")
    report.extend(table_rows)

    print("\n".join(report))

if __name__ == "__main__":
    main()
