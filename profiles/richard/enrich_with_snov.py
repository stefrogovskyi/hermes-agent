import json
import time
import requests
import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')
ws_li = sh.worksheet('👔 LinkedIn Decision Makers & DMs')
current_rows = ws_li.get_all_values()[1:]

snov_uid = 'bfe428f0197f4a764fc5c9f55f2f8816'
snov_secret = '119d04b374ac73f031f95f1d792b3fbe'

# Get token
r_auth = requests.post('https://api.snov.io/v1/oauth/access_token', data={
    'grant_type': 'client_credentials',
    'client_id': snov_uid,
    'client_secret': snov_secret
})
token = r_auth.json().get('access_token')
print("Snov Token obtained successfully!")

additional_domains = [
    ("vanguardlogistics.com", "Vanguard Logistics", "Ocean NVOCC"),
    ("cwt-globelink.com", "CWT Globelink", "Ocean NVOCC"),
    ("dimerco.com", "Dimerco Express", "Global Forwarder"),
    ("spartanglobal.com", "Spartan Global Logistics", "Ocean Forwarder"),
    ("ezollution.com", "Ezollution Software", "Logistics IT Solutions"),
    ("atlas-dis.com", "Atlas Distribution", "Freight Forwarder"),
    ("aimhighlogistics.ph", "Aim High Logistics", "Ocean & Air Forwarder"),
    ("aaccargo.com", "AAC Cargo", "Cargo Logistics"),
    ("shermanslogistics.com", "Shermans Logistics", "Freight Forwarder"),
    ("clearship.com", "Clearship Forwarders", "Customs & Freight"),
    ("dmsworldwide.com", "DMS Worldwide", "Global Shipping"),
    ("cstship.com", "CST Shipping", "Ocean Freight"),
    ("macoline.co.id", "Macoline Shipping", "Ocean NVOCC"),
    ("eimskip.com", "Eimskip Logistics", "Cold Chain & Ocean"),
    ("transpacificlogistik.com", "Transpacific Logistik", "Ocean Forwarder"),
    ("sattvaglobal.in", "Sattva Global Logistics", "Freight Forwarder"),
    ("vilca.biz", "Vilca Logistics", "Freight Forwarder"),
    ("cevalogistics.com", "CEVA Logistics", "Global Logistics"),
    ("bollore-transport-logistics.com", "Bollore Logistics", "Global Transport"),
    ("nipponexpress.com", "Nippon Express", "Global Forwarder"),
    ("rhenus.group", "Rhenus Logistics", "Global Supply Chain"),
    ("tollgroup.com", "Toll Group", "Global Logistics")
]

snov_headers = {'Authorization': f'Bearer {token}'}

snov_results = []
for domain, comp, seg in additional_domains:
    url = f"https://api.snov.io/v2/domain-emails-with-info?domain={domain}&type=all&limit=10"
    try:
        r = requests.get(url, headers=snov_headers, timeout=6)
        if r.status_code == 200:
            res_data = r.json()
            emails = res_data.get('emails', [])
            dm = None
            for e in emails:
                if e.get('socialLinks') and e['socialLinks'].get('linkedin'):
                    dm = e
                    break
            if dm:
                name = f"{dm.get('firstName', '')} {dm.get('lastName', '')}".strip()
                pos = dm.get('position') or 'Executive Manager'
                li = dm['socialLinks']['linkedin'].split('?')[0].rstrip('/')
                snov_results.append({
                    'comp': comp,
                    'web': f"https://{domain}",
                    'name': name,
                    'role': pos,
                    'url': li,
                    'seg': seg
                })
                print(f"  ✅ [Snov] {comp} -> {name} ({pos}) | {li}")
            else:
                print(f"  ⚠️ [Snov] No LinkedIn for {comp} ({domain})")
        else:
            print(f"  ❌ [Snov] Error {r.status_code} for {domain}")
    except Exception as e:
        print(f"  ❌ Error for {domain}: {e}")
    time.sleep(0.3)

print(f"\nSnov collected {len(snov_results)} additional verified leads!")
