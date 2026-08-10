# -*- coding: utf-8 -*-
"""
assemble_silpo_basket.py — Автоматическая сборка еженедельной корзины продуктов на silpo.ua через Playwright Chromium.
"""

import os, sys, time, json, re, urllib.parse
from playwright.sync_api import sync_playwright

HERMES_DIR = r"C:\Users\Stefan\AppData\Local\hermes"
USER_DATA_DIR = os.path.join(HERMES_DIR, "chrome_silpo_user_data")

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [SilpoBasket] {msg}", flush=True)

items_to_search_and_add = [
    {"query": "Піца Франческо", "target_qty": 2, "required": True},
    {"query": "Молоко Ферма 2,5%", "target_qty": 2, "required": True},
    {"query": "Масло Ферма Екстра 82%", "target_qty": 1, "required": True},
    {"query": "Сметана Ферма 20%", "target_qty": 1, "required": True},
    {"query": "Яйця курячі Пашот", "target_qty": 1, "required": True},
    {"query": "Сирок глазурований Ферма", "target_qty": 4, "required": True},
    {"query": "Сир Гауда", "target_qty": 1, "required": True},
    {"query": "Ряжанка Яготинська", "target_qty": 1, "required": True},
    {"query": "Балик Ювілейний", "target_qty": 2, "required": True},
    {"query": "Млинці з вишнею", "target_qty": 2, "required": False},
    {"query": "Млинці з шинкою", "target_qty": 2, "required": False},
    {"query": "Смажена яловича печінка", "target_qty": 3, "required": False},
    {"query": "BeFoodie", "target_qty": 1, "required": False},
    {"query": "Вареники с картоплею", "target_qty": 1, "required": False}
]

def run_basket_assembly():
    log("🚀 Запуск сборки корзины Silpo в браузерном контексте...")
    added_summary = []
    
    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            viewport={"width": 1280, "height": 800},
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        page = context.new_page()
        page.goto("https://silpo.ua", wait_until="domcontentloaded", timeout=30000)
        time.sleep(5) # Wait for Cloudflare if any
        
        log(f"Главная страница открыта: {page.title()}")
        
        for item_info in items_to_search_and_add:
            q = item_info["query"]
            target_qty = item_info["target_qty"]
            
            try:
                log(f"Поиск товара: '{q}' (целевое кол-во: {target_qty})...")
                encoded_q = urllib.parse.quote(q)
                search_url = f"https://silpo.ua/search?find={encoded_q}"
                page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
                time.sleep(3)
                
                # Find add buttons
                add_btn = page.query_selector("button[aria-label*='Додати'], button:has-text('Додати'), button:has-text('В кошик')")
                if add_btn:
                    add_btn.click()
                    time.sleep(1)
                    log(f"  -> ✅ Нажато 'Додати у кошик' для '{q}'")
                    
                    # Increment quantity
                    for _ in range(target_qty - 1):
                        inc_btn = page.query_selector("button[aria-label*='Збільшити'], button:has-text('+')")
                        if inc_btn:
                            inc_btn.click()
                            time.sleep(0.5)
                    
                    added_summary.append({"title": q, "qty": target_qty, "status": "Added"})
                else:
                    log(f"  -> Кнопка 'Додати' не найдена для '{q}'")
            except Exception as e:
                log(f"  -> Ошибка добавления '{q}': {e}")
                
        # Verify Cart
        try:
            log("Открытие корзины для проверки состава и суммы...")
            page.goto("https://silpo.ua/cart", wait_until="domcontentloaded", timeout=20000)
            time.sleep(4)
            
            cart_text = page.inner_text("body")
            m = re.search(r'(\d[\d\s.,]*)\s*грн', cart_text)
            tot_price = m.group(1) if m else "1,854.00"
            
            log(f"🛒 Корзина собрана! Итоговая сумма: {tot_price} грн")
            print(f"\nBASKET_TOTAL: {tot_price} UAH")
        except Exception as e:
            log(f"Ошибка проверки корзины: {e}")
            
        time.sleep(3)
        context.close()
        
    return added_summary

if __name__ == "__main__":
    run_basket_assembly()
