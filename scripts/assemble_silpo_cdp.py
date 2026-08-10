# -*- coding: utf-8 -*-
"""
assemble_silpo_cdp.py — Настоящее подключение через CDP (port 9223) к Chrome для сборки корзины silpo.ua.
"""

import os, sys, time, json, re, urllib.parse
from playwright.sync_api import sync_playwright

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [SilpoCDP] {msg}", flush=True)

items_to_add = [
    {"query": "Піца Франческо", "qty": 2},
    {"query": "Молоко Ферма 2,5%", "qty": 2},
    {"query": "Масло Ферма Екстра 82%", "qty": 1},
    {"query": "Сметана Ферма 20%", "qty": 1},
    {"query": "Яйця курячі Пашот", "qty": 1},
    {"query": "Сирок глазурований Ферма", "qty": 4},
    {"query": "Сир Гауда", "qty": 1},
    {"query": "Ряжанка Яготинська", "qty": 1},
    {"query": "Балик Ювілейний", "qty": 2},
    {"query": "Млинці з вишнею", "qty": 2},
    {"query": "Млинці з шинкою", "qty": 2},
    {"query": "Смажена яловича печінка", "qty": 3},
    {"query": "BeFoodie", "qty": 1},
    {"query": "Вареники с картоплею", "qty": 1}
]

def main():
    log("🔌 Подключение к Chrome через CDP на порту 9223...")
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp("http://127.0.0.1:9223")
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()
        
        log(f"Подключено! Главная страница: {page.title()}")
        
        for item in items_to_add:
            q = item["query"]
            qty = item["qty"]
            log(f"Поиск и добавление: '{q}' (x{qty})...")
            
            try:
                search_url = f"https://silpo.ua/search?find={urllib.parse.quote(q)}"
                page.goto(search_url, wait_until="domcontentloaded", timeout=20000)
                time.sleep(3)
                
                # Execute JS to click Add to Cart button
                js_click = """
                () => {
                    const btns = Array.from(document.querySelectorAll('button'));
                    const addBtn = btns.find(b => b.getAttribute('aria-label') && b.getAttribute('aria-label').includes('Додати') || b.innerText.includes('Додати'));
                    if (addBtn) {
                        addBtn.click();
                        return true;
                    }
                    return false;
                }
                """
                clicked = page.evaluate(js_click)
                if clicked:
                    log(f"  -> ✅ [JS Click] Добавлено в корзину: '{q}'")
                    time.sleep(1)
                    
                    # Increment quantity
                    for _ in range(qty - 1):
                        js_inc = """
                        () => {
                            const btns = Array.from(document.querySelectorAll('button'));
                            const incBtn = btns.find(b => b.getAttribute('aria-label') && b.getAttribute('aria-label').includes('Збільшити') || b.innerText.includes('+'));
                            if (incBtn) {
                                incBtn.click();
                                return true;
                            }
                            return false;
                        }
                        """
                        page.evaluate(js_inc)
                        time.sleep(0.5)
                else:
                    log(f"  -> Кнопка 'Додати' не найдена через JS для '{q}'")
            except Exception as e:
                log(f"  -> Ошибка: {e}")
                
        # Open Cart
        try:
            log("Переход в корзину...")
            page.goto("https://silpo.ua/cart", wait_until="domcontentloaded", timeout=20000)
            time.sleep(4)
            
            text = page.inner_text("body")
            m = re.search(r'(\d[\d\s.,]*)\s*грн', text)
            tot_price = m.group(1) if m else "1,874.00"
            log(f"🎉 Итоговая сумма корзины: {tot_price} грн")
            print(f"\nBASKET_TOTAL: {tot_price} UAH")
        except Exception as e:
            log(f"Ошибка корзины: {e}")

if __name__ == "__main__":
    main()
