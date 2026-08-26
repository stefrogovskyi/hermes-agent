#!/usr/bin/env python3
"""
Renders an HTML template into a high-resolution 2x Retina PNG for LinkedIn / X social media cards.
Usage: python3 render-social-card.py <template_html_path> <output_png_path> [width] [height]
"""
import sys
import os
from playwright.sync_api import sync_playwright

def render_card(html_path: str, output_path: str, width: int = 1200, height: int = 675):
    if not os.path.exists(html_path):
        print(f"Error: HTML template not found at {html_path}")
        sys.exit(1)

    abs_html = os.path.abspath(html_path)
    abs_out = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(abs_out), exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-setuid-sandbox"])
        context = browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=2 # 2x Retina output
        )
        page = context.new_page()
        page.goto(f"file://{abs_html}")
        # Allow Fontshare web fonts (Ranade, Switzer) to fully load
        page.wait_for_timeout(2000)
        page.screenshot(path=abs_out, type="png")
        browser.close()

    print(f"✓ Rendered Retina PNG ({width*2}x{height*2}) to: {abs_out}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 render-social-card.py <html_path> <output_path> [width] [height]")
        sys.exit(1)
    
    html_f = sys.argv[1]
    out_f = sys.argv[2]
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
    h = int(sys.argv[4]) if len(sys.argv) > 4 else 675

    render_card(html_f, out_f, w, h)
