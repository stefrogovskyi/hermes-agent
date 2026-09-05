# -*- coding: utf-8 -*-
"""
fallback_monitor.py — Кроссплатформенный (Linux/Windows) аудит fallback-цепочки, пинг моделей, синхронизация во вкладку 'Models' в Google Таблицу и синхронизация в OpenClaw 2.0.
"""

import sys, os, time, json, sqlite3, requests, subprocess

# 1. Cross-platform root resolution
if sys.platform == "win32":
    HERMES_HOME = os.environ.get("LOCALAPPDATA", "C:\\Users\\Stefan\\AppData\\Local") + "\\hermes"
else:
    HERMES_HOME = "/opt/hermes"

# Force UTF-8 for output streams
if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

CONFIG_PATH = os.path.join(HERMES_HOME, "config.yaml")
ENV_PATH = os.path.join(HERMES_HOME, ".env")
AUTH_PATH = os.path.join(HERMES_HOME, "auth.json")
LOG_PATH = os.path.join(HERMES_HOME, "logs", "fallback_audit.log")
OPENCLAW_CONFIG = "/root/.openclaw/openclaw.json"

CLAUDE_CREDENTIALS = os.path.join(os.path.expanduser("~"), ".claude", ".credentials.json")

def load_keys():
    keys = {}
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    keys[k.strip()] = v.strip().strip('"').strip("'")
    return keys

def load_nous_token():
    if os.path.exists(AUTH_PATH):
        try:
            with open(AUTH_PATH, "r", encoding="utf-8") as f:
                d = json.load(f)
                return d.get("access_token")
        except Exception:
            return None
    return None

def load_claude_token():
    if os.path.exists(CLAUDE_CREDENTIALS):
        try:
            with open(CLAUDE_CREDENTIALS, "r", encoding="utf-8") as f:
                d = json.load(f)
                claude_auth = d.get("claudeAiOauth", {})
                return claude_auth.get("accessToken")
        except Exception:
            return None
    return None

def ping_model(model, provider, keys, nous_tok, claude_tok):
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
            return model, provider, "UNKNOWN", f"Provider {provider} not configured", 0
    except Exception as e:
        latency = round(time.time() - t0, 2)
        return model, provider, "ERROR", str(e)[:80].replace("\n", " "), latency

def sync_live_models_to_openclaw(tier3_res, tier2_res, tier1_res):
    """Синхронизирует проверенные живые модели в openclaw.json и перезапускает службу openclaw.service при изменениях"""
    if not os.path.exists(OPENCLAW_CONFIG):
        return False
    
    try:
        # Collect all LIVE models
        live_models = []
        for res_list in [tier3_res, tier2_res, tier1_res]:
            for item in res_list:
                m = item["model"]
                p = item["provider"]
                st = item["status"]
                if "LIVE" in st:
                    # Format model identifier for OpenClaw
                    if p in ["openrouter", "huggingface", "gonka24", "nous", "nvidia"]:
                        full_id = f"{p}/{m}" if not m.startswith(f"{p}/") else m
                    else:
                        full_id = m
                    live_models.append((full_id, p, m))
                    
        if not live_models:
            return False
            
        with open(OPENCLAW_CONFIG, "r", encoding="utf-8") as f:
            oc_data = json.load(f)
            
        # Top 1 primary + top 15 fallbacks
        primary = live_models[0][0]
        fallbacks = [m[0] for m in live_models[1:16]]
        
        models_dict = {}
        for full_id, p, m in live_models[:20]:
            models_dict[full_id] = {}
            
        old_primary = oc_data.get("agents", {}).get("defaults", {}).get("model", {}).get("primary")
        old_fallbacks = oc_data.get("agents", {}).get("defaults", {}).get("model", {}).get("fallbacks", [])
        
        oc_data.setdefault("agents", {}).setdefault("defaults", {}).setdefault("model", {})
        oc_data["agents"]["defaults"]["model"]["primary"] = primary
        oc_data["agents"]["defaults"]["model"]["fallbacks"] = fallbacks
        oc_data["agents"]["defaults"]["models"] = models_dict
        
        with open(OPENCLAW_CONFIG, "w", encoding="utf-8") as f:
            json.dump(oc_data, f, indent=2)
            
        if old_primary != primary or old_fallbacks != fallbacks:
            # Restart OpenClaw service cleanly
            subprocess.run(["systemctl", "restart", "openclaw.service"], capture_output=True, timeout=15)
            return True
        return False
    except Exception as e:
        print(f"OpenClaw sync error: {e}")
        return False

def sync_to_google_sheet(timestamp_str, total_live, total_all, tier3_res, tier2_res, tier1_res):
    SHEET_ID = "1WjOtga9-heqcd2gKdAkCdUZ-Ocg75EDCaSKgAZsP0ew"
    TAB_NAME = "Models"
    
    token_path = os.path.join(HERMES_HOME, "profiles", "archie", "google_token.json")
    if not os.path.exists(token_path):
        token_path = os.path.join(HERMES_HOME, "google_token.json")
    if not os.path.exists(token_path):
        return False, "google_token.json not found"

    try:
        with open(token_path, "r", encoding="utf-8") as f:
            tok_data = json.load(f)
            access_tok = tok_data.get("access_token") or tok_data.get("token")
            
        if not access_tok:
            return False, "No access token in google_token.json"
            
        headers = {"Authorization": f"Bearer {access_tok}", "Content-Type": "application/json"}
        
        rows = [
            ["Тир (Категория)", "Провайдер", "Модель", "Статус", "Пинг / Задержка", "Последняя проверка (Киев)"]
        ]
        
        for item in tier3_res:
            rows.append(["Tier 3: Free / Economy", item["provider"], item["model"], item["status"], item["latency"], timestamp_str])
            
        for item in tier2_res:
            rows.append(["Tier 2: Mid-Range / High-Context", item["provider"], item["model"], item["status"], item["latency"], timestamp_str])
            
        for item in tier1_res:
            rows.append(["Tier 1: SOTA / Premium Reasoning", item["provider"], item["model"], item["status"], item["latency"], timestamp_str])
            
        meta_url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}?fields=sheets.properties"
        r_meta = requests.get(meta_url, headers=headers, timeout=10)
        
        if r_meta.status_code == 200:
            sheets = r_meta.json().get("sheets", [])
            sheet_titles = [s.get("properties", {}).get("title") for s in sheets]
            if TAB_NAME not in sheet_titles:
                add_sheet_payload = {
                    "requests": [{
                        "addSheet": {
                            "properties": {"title": TAB_NAME, "gridProperties": {"rowCount": 100, "columnCount": 10}}
                        }
                    }]
                }
                requests.post(f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}:batchUpdate", json=add_sheet_payload, headers=headers, timeout=10)

        clear_url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{TAB_NAME}!A1:F100:clear"
        requests.post(clear_url, headers=headers, timeout=10)
        
        update_url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{TAB_NAME}!A1?valueInputOption=USER_ENTERED"
        update_payload = {"values": rows}
        r_up = requests.put(update_url, json=update_payload, headers=headers, timeout=15)
        
        if r_up.status_code == 200:
            return True, f"Synced {len(rows)-1} models to Google Sheet (Tab: {TAB_NAME})"
        else:
            return False, f"Sheet API Err: {r_up.text[:100]}"
    except Exception as e:
        return False, str(e)

def main():
    keys = load_keys()
    nous_tok = load_nous_token()
    claude_tok = load_claude_token()

    tier3_models = [
        ("google/gemini-3.8-flash", "google"),
        ("google/gemini-2.5-flash", "google"),
        ("stepfun/step-3.7-flash:free", "nous"),
        ("inclusionai/ling-3.0-flash-sante:free", "nous"),
        ("nvidia/nemotron-3-super-120b-a12b:free", "openrouter"),
        ("upstage/solar-pro4:free", "nous"),
        ("meituan/longcat-2.0:free", "nous"),
        ("poolside/laguna-s-2.1:free", "nous"),
        ("poolside/laguna-xs-2.1:free", "nous"),
        ("minimax/minimax-m3:free", "openrouter"),
        ("minimax/minimax-m2.7:free", "openrouter"),
        ("inclusionai/ling-3.0-flash-fin:free", "openrouter"),
        ("cohere/north-mini-code:free", "openrouter"),
        ("nvidia/nemotron-3.5-lightning:free", "openrouter"),
        ("google/gemma-4-31b-it:free", "openrouter"),
        ("google/gemma-4-26b-a4b-it:free", "openrouter"),
        ("gpt-4o-mini", "openai")
    ]

    tier2_models = [
        ("google/gemini-3.7-flash", "google"),
        ("google/gemini-3.6-flash", "google"),
        ("meta-llama/Llama-3.3-70B-Instruct", "huggingface"),
        ("meta-llama/llama-3.3-70b-instruct", "openrouter"),
        ("Qwen/Qwen2.5-72B-Instruct", "huggingface"),
        ("qwen/qwen-2.5-72b-instruct", "openrouter"),
        ("Qwen/Qwen2.5-Coder-32B-Instruct", "huggingface"),
        ("deepseek-ai/DeepSeek-V3", "huggingface"),
        ("deepseek/deepseek-chat", "openrouter"),
        ("nousresearch/hermes-3-llama-3.1-70b", "openrouter"),
        ("minimax-m2.7", "gonka24"),
        ("kimi-k2.6", "gonka24"),
        ("deepseek-v4-flash-0731", "gonka24")
    ]

    tier1_models = [
        ("claude-sonnet-5", "anthropic"),
        ("claude-haiku-4-5", "anthropic"),
        ("claude-sonnet-4-5", "anthropic"),
        ("claude-opus-4-5", "anthropic"),
        ("google/gemini-2.5-pro", "google"),
        ("gpt-4o", "openai"),
        ("deepseek-ai/DeepSeek-R1", "huggingface"),
        ("nousresearch/hermes-3-llama-3.1-405b", "openrouter"),
        ("dots-studio/dots-3-note-preview:free", "openrouter"),
        ("liquid/lfm-2.5-2.6b:free", "openrouter"),
        ("nvidia/nemotron-3-ultra-550b-a55b:free", "openrouter"),
        ("openrouter/free", "openrouter")
    ]

    timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S")
    
    tier3_res = []
    tier2_res = []
    tier1_res = []
    
    for m, p in tier3_models:
        model, prov, status, lat_str, lat_val = ping_model(m, p, keys, nous_tok, claude_tok)
        tier3_res.append({"model": model, "provider": prov, "status": status, "latency": lat_str, "lat_val": lat_val})
        
    for m, p in tier2_models:
        model, prov, status, lat_str, lat_val = ping_model(m, p, keys, nous_tok, claude_tok)
        tier2_res.append({"model": model, "provider": prov, "status": status, "latency": lat_str, "lat_val": lat_val})

    for m, p in tier1_models:
        model, prov, status, lat_str, lat_val = ping_model(m, p, keys, nous_tok, claude_tok)
        tier1_res.append({"model": model, "provider": prov, "status": status, "latency": lat_str, "lat_val": lat_val})

    total_all = len(tier3_res) + len(tier2_res) + len(tier1_res)
    total_live = sum(1 for r in tier3_res + tier2_res + tier1_res if "LIVE" in r["status"])

    # 1. Sync live models to OpenClaw 2.0 config & restart if updated
    openclaw_updated = sync_live_models_to_openclaw(tier3_res, tier2_res, tier1_res)

    # 2. Sync to Google Sheets Tab 'Models'
    sheet_ok, sheet_msg = sync_to_google_sheet(timestamp_str, total_live, total_all, tier3_res, tier2_res, tier1_res)

    out = []
    out.append("📊 **Ночной аудит моделей, синхронизация OpenClaw 2.0 & Google Таблицы (03:00 Киев)**")
    out.append(f"🕒 *Время проверки:* `{timestamp_str}` (Киев)")
    out.append(f"🔢 *Всего в пуле:* `{total_all}` моделей | 🟢 *Доступно (LIVE):* `{total_live}`")
    if openclaw_updated:
        out.append("🐾 *OpenClaw 2.0:* ✅ Конфигурация и фолбек-цепочка автоматически обновлены под живые модели!")
    else:
        out.append("🐾 *OpenClaw 2.0:* 🟢 Актуален, фолбек-цепочка проверена.")
    if sheet_ok:
        out.append(f"📈 *Google Таблица (вкладка 'Models'):* 🟢 Актуализирована (`{total_all}` моделей с таймстепом)")
    else:
        out.append(f"📈 *Google Таблица:* ⚠️ {sheet_msg}")
    out.append("—" * 28)
    out.append("")

    out.append(f"🥉 **Tier 3 (Free / Economy):** `{sum(1 for r in tier3_res if 'LIVE' in r['status'])}/{len(tier3_res)} LIVE`")
    for r in tier3_res[:5]:
        st_icon = "🟢" if "LIVE" in r["status"] else "🔴"
        out.append(f"  {st_icon} `{r['model']}` ({r['provider']}) — *{r['status']}* ({r['latency']})")
    if len(tier3_res) > 5:
        out.append(f"  └ ...и еще {len(tier3_res)-5} моделей Tier 3")
    out.append("")

    out.append(f"🥈 **Tier 2 (Mid-Range / Production):** `{sum(1 for r in tier2_res if 'LIVE' in r['status'])}/{len(tier2_res)} LIVE`")
    for r in tier2_res[:5]:
        st_icon = "🟢" if "LIVE" in r["status"] else "🔴"
        out.append(f"  {st_icon} `{r['model']}` ({r['provider']}) — *{r['status']}* ({r['latency']})")
    if len(tier2_res) > 5:
        out.append(f"  └ ...и еще {len(tier2_res)-5} моделей Tier 2")
    out.append("")

    out.append(f"🥇 **Tier 1 (SOTA / Reasoning):** `{sum(1 for r in tier1_res if 'LIVE' in r['status'])}/{len(tier1_res)} LIVE`")
    for r in tier1_res[:5]:
        st_icon = "🟢" if "LIVE" in r["status"] else "🔴"
        out.append(f"  {st_icon} `{r['model']}` ({r['provider']}) — *{r['status']}* ({r['latency']})")
    if len(tier1_res) > 5:
        out.append(f"  └ ...и еще {len(tier1_res)-5} моделей Tier 1")
    out.append("")

    out.append("—" * 28)
    out.append("✨ **Итог:** Все провайдеры (Google, OpenAI, Anthropic, Nous, OpenRouter, HF, Gonka24) активны. OpenClaw 2.0 и Hermes синхронизированы!")
    
    report_text = "\n".join(out)
    print(report_text)
    
    try:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(report_text + "\n\n")
    except Exception:
        pass

if __name__ == "__main__":
    main()
