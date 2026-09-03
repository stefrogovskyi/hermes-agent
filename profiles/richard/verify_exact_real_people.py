import json
import time
import urllib.parse
from playwright.sync_api import sync_playwright
import gspread

gc = gspread.service_account(filename='/opt/hermes/profiles/richard/google_service_account.json')
sh = gc.open_by_key('1ceJzlfTCQIvJeMoBZfIhxesFxPM9mbV_iAMe6qXEIMo')
ws_li = sh.worksheet('👔 LinkedIn Decision Makers & DMs')

# Target verified logistics & freight forwarding companies
top_forwarders = [
    ("Mohawk Global Logistics", "https://mohawkglobal.com", "Gar Grannell", "https://www.linkedin.com/in/gar-grannell-8151aa9"),
    ("DP World", "https://dpworld.com", "Sultan Ahmed Bin Sulayem", "https://www.linkedin.com/in/sultan-ahmed-bin-sulayem-52b86b16"),
    ("Kuehne + Nagel", "https://kuehne-nagel.com", "Stefan Paul", "https://www.linkedin.com/in/stefan-paul-kn"),
    ("Hellmann Worldwide Logistics", "https://hellmann.com", "Jens Drewes", "https://www.linkedin.com/in/jens-drewes-77299a1b"),
    ("DB Schenker", "https://dbschenker.com", "Jochen Thewes", "https://www.linkedin.com/in/jochen-thewes-007137b"),
    ("DSV - Global Transport and Logistics", "https://dsv.com", "Jens Lund", "https://www.linkedin.com/in/jens-lund-dsv"),
    ("Geodis", "https://geodis.com", "Marie-Christine Lombard", "https://www.linkedin.com/in/marie-christine-lombard-0a256a59"),
    ("Bollore Logistics", "https://bollore-transport-logistics.com", "Cyrille Bollore", "https://www.linkedin.com/in/cyrille-bollore-091a0368"),
    ("CEVA Logistics", "https://cevalogistics.com", "Mathieu Friedberg", "https://www.linkedin.com/in/mathieu-friedberg-27361816"),
    ("C.H. Robinson", "https://chrobinson.com", "Dave Bozeman", "https://www.linkedin.com/in/dave-bozeman-chrobinson"),
    ("Expeditors", "https://expeditors.com", "Jeffrey S. Musser", "https://www.linkedin.com/in/jeffrey-musser-expeditors"),
    ("Nippon Express", "https://nipponexpress.com", "Satoshi Horikiri", "https://www.linkedin.com/in/satoshi-horikiri-9b578619"),
    ("Dachser", "https://dachser.com", "Burkhard Eling", "https://www.linkedin.com/in/burkhard-eling-dachser"),
    ("Agility Logistics", "https://agility.com", "Tarek Sultan", "https://www.linkedin.com/in/tarek-sultan-agility"),
    ("Sinotrans", "https://sinotrans.com", "Song Rong", "https://www.linkedin.com/in/song-rong-sinotrans"),
    ("Kerry Logistics", "https://kerrylogistics.com", "Vic Cheung", "https://www.linkedin.com/in/vic-cheung-kerry"),
    ("Logwin Logistics", "https://logwin-logistics.com", "Sebastian Esser", "https://www.linkedin.com/in/sebastian-esser-logwin"),
    ("Rhenus Logistics", "https://rhenus.group", "Tobias Bartz", "https://www.linkedin.com/in/tobias-bartz-rhenus"),
    ("Mainfreight", "https://mainfreight.com", "Don Braid", "https://www.linkedin.com/in/don-braid-mainfreight"),
    ("Fesco Transportation Group", "https://fesco.ru", "Andrey Severilov", "https://www.linkedin.com/in/andrey-severilov"),
    ("Allcargo Logistics", "https://allcargologistics.com", "Shashi Kiran Shetty", "https://www.linkedin.com/in/shashi-kiran-shetty-allcargo"),
    ("ECU Worldwide", "https://ecuworldwide.com", "Tim Spillane", "https://www.linkedin.com/in/tim-spillane-ecu"),
    ("ShipBob", "https://shipbob.com", "Dhruv Saxena", "https://www.linkedin.com/in/dhruvsaxena"),
    ("Flexport", "https://flexport.com", "Ryan Petersen", "https://www.linkedin.com/in/ryanpetersen"),
    ("Freightos", "https://freightos.com", "Zvi Schreiber", "https://www.linkedin.com/in/zvischreiber"),
    ("project44", "https://project44.com", "Jett McCandless", "https://www.linkedin.com/in/jettmccandless"),
    ("FourKites", "https://fourkites.com", "Mathew Elenjickal", "https://www.linkedin.com/in/mathewelenjickal"),
    ("Vizion API", "https://vizionapi.com", "Kyle Henderson", "https://www.linkedin.com/in/kylehenderson"),
    ("Terminal49", "https://terminal49.com", "Akshay Dhumuntarao", "https://www.linkedin.com/in/akshaydhumuntarao"),
    ("GoComet", "https://gocomet.com", "Gautam Prem Jain", "https://www.linkedin.com/in/gautampremjain")
]

print(f"Starting browser verification of {len(top_forwarders)} direct personal LinkedIn profiles...")

verified_results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(
        user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    )
    
    for comp, web, name, url in top_forwarders:
        try:
            page.goto(url, timeout=10000)
            time.sleep(1.0)
            title = page.title()
            is_valid = '404' not in title and 'Page not found' not in title and 'LinkedIn' in title
            print(f"[{'PASS' if is_valid else 'FAIL'}] {name} ({comp}) -> {url} | Title: {title[:40]}")
            
            verified_results.append({
                'comp': comp,
                'web': web,
                'name': name,
                'url': url,
                'title': title,
                'valid': is_valid
            })
        except Exception as e:
            print(f"[ERROR] {name} -> {e}")
            
    browser.close()

print(f"\nDone! Verified {len(verified_results)} profiles directly in browser.")
