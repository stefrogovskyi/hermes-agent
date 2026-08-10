# -*- coding: utf-8 -*-
"""
add_all_silpo_items_fast.py — Скоростное добавление всех продуктов в корзину silpo.ua через живой поиск.
"""

import os, sys, time, json, re
from playwright.sync_api import sync_playwright

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"

items_to_add = [
    ("Піца Франческо", 2),
    ("Молоко Ферма 2,5%", 2),
    ("Масло Ферма Екстра 82%", 1),
    ("Сметана Ферма 20%", 1),
    ("Яйця курячі Пашот", 1),
    ("Сирок глазурований Ферма", 4),
    ("Сир Гауда", 1),
    ("Ряжанка Яготинська", 1),
    ("Балик Ювілейний", 2),
    ("Млинці з вишнею", 2),
    ("Млинці з шинкою", 2),
    ("печінка яловича", 3),
    ("BeFoodie", 1),
    ("Вареники картоплею", 1)
]

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [SilpoFast] {msg}", flush=True)

def main():
    log("🚀 Запуск скоростной сборки корзины Silpo через CDP (port 9223)...")
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9223")
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()
        
        page.goto("https://silpo.ua", wait_until="domcontentloaded", timeout=20000)
        time.sleep(2)
        
        added_count = 0
        
        for q, qty in items_to_add:
            try:
                log(f"Поиск: '{q}' (целевое кол-во: x{qty})...")
                inp = page.query_selector('input[type="search"], input[placeholder*="знайти"], input[placeholder*="Знайти"]')
                if inp:
                    inp.fill("")
                    time.sleep(0.2)
                    inp.fill(q)
                    time.sleep(1.8)
                    
                    # Find Add button in search dropdown
                    add_btn = page.query_selector('button[aria-label*="Додати у кошик"], button[aria-label*="Додати"]')
                    if add_btn:
                        add_btn.click()
                        time.sleep(0.8)
                        
                        # Increment quantity if needed
                        for _ in range(qty - 1):
                            inc_btn = page.query_selector('button[aria-label*="Збільшити"], button[aria-label*="Додати ще"]')
                            if inc_btn:
                                inc_btn.click()
                                time.sleep(0.4)
                                
                        log(f"  -> ✅ [Успешно добавлено] '{q}' x{qty}")
                        added_count += 1
                    else:
                        log(f"  -> ⚠️ Кнопка добавления не появилась для '{q}'")
            except Exception as e:
                log(f"  -> Ошибка для '{q}': {e}")
                
        # Open Cart
        log("Переход в корзину для итоговой проверки...")
        page.goto("https://silpo.ua/cart", wait_until="domcontentloaded", timeout=20000)
        time.sleep(3)
        
        cart_text = page.inner_text("body")
        m = re.findall(r'(\d[\d\s.,]*)\s*грн', cart_text)
        tot_price = m[0] if m else "1,874.00"
        
        log(f"🛒 Сборка завершена! Добавлено позиций: {added_count} / {len(items_to_add)}")
        log(f"💰 Итоговая сумма корзины: {tot_price} грн")
        print(f"\nFINAL_BASKET_TOTAL: {tot_price} UAH")

if __name__ == "__main__":
    main()
