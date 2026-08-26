import urllib.request, json, time, sys

container = sys.argv[1] if len(sys.argv) > 1 else "MSCU8142203"
api_key = "tmcp_039ceee30bfbba0bf315726730c325e5d3a449768c4b230e"

url_native = f"https://navo24-tracking-api-staging.fly.dev/v1/containers/{container}"
url_compat = f"https://navo24-tracking-api-staging.fly.dev/compat/searates/tracking?api_key={api_key}&number={container}&sealine=MSCU"

headers_native = {
    'Accept': 'application/json',
    'Authorization': f"Bearer {api_key}",
    'X-API-Key': api_key,
    'User-Agent': 'Hermes-Ops/1.0'
}

max_attempts = 30 # up to 5 minutes
for i in range(1, max_attempts + 1):
    time.sleep(10)
    # Check native v1
    try:
        req = urllib.request.Request(url_native, headers=headers_native)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            if data.get('ok') is True or data.get('containers') or data.get('data'):
                print(f"✅ НАЙДЕНЫ ДАННЫЕ ПО КОНТЕЙНЕРУ {container}!\n")
                print(json.dumps(data, indent=2, ensure_ascii=False))
                sys.exit(0)
    except Exception:
        pass
        
    # Check compat
    try:
        req_c = urllib.request.Request(url_compat, headers={'Accept': 'application/json'})
        with urllib.request.urlopen(req_c, timeout=12) as resp:
            data_c = json.loads(resp.read().decode('utf-8'))
            if data_c.get('status') == 'success' and data_c.get('data', {}).get('containers'):
                print(f"✅ НАЙДЕНЫ ДАННЫЕ ПО КОНТЕЙНЕРУ {container} (SeaRates compat format)!\n")
                print(json.dumps(data_c, indent=2, ensure_ascii=False))
                sys.exit(0)
    except Exception:
        pass

print(f"⚠️ Время ожидания первого ответа от MSC для {container} истекло (5 минут).")
sys.exit(0)
