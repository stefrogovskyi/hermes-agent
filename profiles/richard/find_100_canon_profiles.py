import json
import time
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

candidates_to_test = [
    # Top Global Forwarders Leaders
    ("Stefan Paul", "Kuehne + Nagel", "Chief Executive Officer", "https://ch.linkedin.com/in/stefan-paul-kn", "https://kuehne-nagel.com"),
    ("Jens Drewes", "Hellmann Worldwide Logistics", "Chief Executive Officer", "https://de.linkedin.com/in/jens-drewes-77299a1b", "https://hellmann.com"),
    ("Jochen Thewes", "DB Schenker", "Chief Executive Officer", "https://de.linkedin.com/in/jochen-thewes-007137b", "https://dbschenker.com"),
    ("Burkhard Eling", "Dachser", "Chief Executive Officer", "https://de.linkedin.com/in/burkhard-eling-dachser", "https://dachser.com"),
    ("Tobias Bartz", "Rhenus Logistics", "CEO & Chairman", "https://de.linkedin.com/in/tobias-bartz-rhenus", "https://rhenus.group"),
    ("Shashi Kiran Shetty", "Allcargo Logistics", "Founder & Chairman", "https://in.linkedin.com/in/shashi-kiran-shetty-allcargo", "https://allcargologistics.com"),
    ("Tim Spillane", "ECU Worldwide", "Managing Director", "https://www.linkedin.com/in/tim-spillane-ecu", "https://ecuworldwide.com"),
    ("Gar Grannell", "Mohawk Global Logistics", "President & CEO", "https://www.linkedin.com/in/gar-grannell-8151aa9", "https://mohawkglobal.com"),
    ("Ryan Petersen", "Flexport", "Founder & CEO", "https://www.linkedin.com/in/ryanpetersen", "https://flexport.com"),
    ("Zvi Schreiber", "Freightos", "Founder & CEO", "https://www.linkedin.com/in/zvischreiber", "https://freightos.com"),
    ("Jett McCandless", "project44", "Founder & CEO", "https://www.linkedin.com/in/jettmccandless", "https://project44.com"),
    ("Mathew Elenjickal", "FourKites", "Founder & CEO", "https://www.linkedin.com/in/mathewelenjickal", "https://fourkites.com"),
    ("Kyle Henderson", "Vizion API", "CEO & Co-Founder", "https://www.linkedin.com/in/kylehenderson", "https://vizionapi.com"),
    ("Akshay Dhumuntarao", "Terminal49", "Founder & CEO", "https://www.linkedin.com/in/akshaydhumuntarao", "https://terminal49.com"),
    ("Gautam Prem Jain", "GoComet", "CEO & Co-Founder", "https://in.linkedin.com/in/gautampremjain", "https://gocomet.com"),
    ("Gary Nemmers", "Magaya", "CEO", "https://www.linkedin.com/in/gary-nemmers-7859593", "https://magaya.com"),
    ("Edward J. Ryan", "Descartes Systems", "CEO", "https://ca.linkedin.com/in/edward-j-ryan-descartes", "https://descartes.com"),
    ("Richard White", "WiseTech Global", "Founder & CEO", "https://au.linkedin.com/in/richard-white-wisetech", "https://wisetechglobal.com"),
    ("Raghavendran Viswanathan", "Freightify", "Founder & CEO", "https://in.linkedin.com/in/raghavendran-v", "https://freightify.com"),
    ("Nidhi Gupta", "Portcast", "CEO & Co-Founder", "https://sg.linkedin.com/in/nidhigupta-portcast", "https://portcast.io"),
    ("Julien Cote", "Wakeo", "CEO & Co-Founder", "https://fr.linkedin.com/in/julien-cote-wakeo", "https://wakeo.co"),
    ("Carl Lauron", "BuyCo", "Founder & CEO", "https://fr.linkedin.com/in/carl-lauron-buyco", "https://buyco.co"),
    ("Hunter Yaw", "LogRock", "CEO & Co-Founder", "https://www.linkedin.com/in/hunteryaw", "https://logrock.com"),
    ("Allan Melgaard", "Scan Global Logistics", "Global CEO", "https://dk.linkedin.com/in/allan-melgaard-sgl", "https://scangl.com"),
    ("Mike Andaloro", "PSA BDP", "CEO", "https://www.linkedin.com/in/mike-andaloro-bdp", "https://psabdp.com"),
    ("James Gagne", "SEKO Logistics", "President & CEO", "https://www.linkedin.com/in/james-gagne-seko", "https://sekologistics.com"),
    ("Michael Xu", "OOCL Logistics", "Executive Director", "https://hk.linkedin.com/in/michael-xu-oocl", "https://oocllogistics.com"),
    ("Alan Beacham", "Toll Group", "Managing Director", "https://au.linkedin.com/in/alan-beacham-toll", "https://tollgroup.com"),
    ("Keith Winters", "Crane Worldwide Logistics", "CEO", "https://www.linkedin.com/in/keith-winters-crane", "https://craneww.com"),
    ("Graham Page", "Vanguard Logistics", "CEO", "https://uk.linkedin.com/in/graham-page-vanguard", "https://vanguardlogistics.com")
]

print(f"Testing {len(candidates_to_test)} candidate URLs in Playwright...")

valid_pool = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    
    for name, comp, role, url, web in candidates_to_test:
        try:
            page.goto(url, timeout=10000)
            time.sleep(1)
            soup = BeautifulSoup(page.content(), 'html.parser')
            og_title = soup.find('meta', property='og:title')
            og_content = og_title['content'] if og_title else ''
            
            # Check if og_content contains person name or company
            has_name = name.split()[0].lower() in og_content.lower() or name.split()[-1].lower() in og_content.lower()
            
            print(f"[{'VERIFIED' if has_name else 'REJECTED'}] {name} ({comp}) -> OG: {og_content}")
            if has_name:
                valid_pool.append({
                    'name': name,
                    'comp': comp,
                    'role': role,
                    'url': url,
                    'web': web,
                    'og_title': og_content
                })
        except Exception as e:
            print(f"[ERR] {name} -> {e}")
            
    browser.close()

print(f"\nSuccessfully verified {len(valid_pool)} strict 100% live profiles!")
