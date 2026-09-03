import re

title = "SeaRates at LISW25: Meet Us in London"
meta_title = "SeaRates at LISW25: Meet Us in London"
meta_desc = "Connect with SeaRates at London International Shipping Week 2025 (Sep 15-19). Meet our team to discuss logistics tech and supply chain visibility."

body = """Shipping operates on movement, but real progress happens when the industry gathers in one room.

From September 15 to 19, 2025, London International Shipping Week 2025 (LISW25) brings global maritime leaders to London, United Kingdom. The SeaRates team will be present throughout the week to connect with cargo owners and logistics managers looking for practical ways to improve their everyday shipping operations.

The week features an extensive program, including the mid-week IMO Headquarters Headline Conference, gala dinners, receptions, and specialized networking sessions. Agenda discussions will center on pressing industry topics, such as decarbonization strategies, alternative fuel adoption, safety, regulatory compliance, and seafarer crewing and training. Sessions will also explore maritime digital transformation alongside supply chain visibility & resilience under changing global trade dynamics.

Lilia Khovrak and Ekaterina Komarova will represent SeaRates during the event. They will be available to discuss your specific logistics requirements and share guidance on optimizing container shipping with modern software tools.

If you are attending LISW25 and want to review your supply chain setup, reach out to schedule a meeting with our team by emailing sales@searates.com. We look forward to seeing you in London this September.
"""

full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"

errors = []

# Character limits
if len(title) > 60: errors.append(f"Title length {len(title)} > 60")
if len(meta_title) > 60: errors.append(f"Meta-title length {len(meta_title)} > 60")
if len(meta_desc) > 155: errors.append(f"Meta-description length {len(meta_desc)} > 155")

# Rule 1: No em-dashes
if "—" in full_text or "--" in full_text: errors.append("Em-dash found")

# Rule 2: Slop
banned = ["delighted to announce", "glad to break the news", "vital role", "in today's world", "dive into", "seamless", "game-changer", "testament to", "unlock"]
for b in banned:
    if b in full_text.lower(): errors.append(f"Banned slop: {b}")

# Rule 6: Connectors
if "that's why" in full_text.lower() or "which is why" in full_text.lower():
    errors.append("Banned connector")

# Required keywords
keywords = [
    "London International Shipping Week 2025 (LISW25)",
    "Maritime digital transformation",
    "Supply chain visibility & resilience",
    "Decarbonization strategies",
    "IMO Headquarters Headline Conference"
]
for kw in keywords:
    if kw.lower() not in full_text.lower():
        errors.append(f"Missing keyword: {kw}")

# Print findings
print("Validation Results:")
print("Errors:", errors if errors else "PASSED ALL CHECKS!")
print("\nCharacter Counts:")
print(f"Title: {len(title)} chars (Max 60)")
print(f"Meta Title: {len(meta_title)} chars (Max 60)")
print(f"Meta Description: {len(meta_desc)} chars (Max 155)")
