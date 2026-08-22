# Modular Pitch Variation Engine (Anti-Spam Strategy)

## Problem
Messaging algorithms on WhatsApp and SMS gateways detect identical text templates repeated across distinct recipients and flag the sending number as automated spam, leading to shadowbans or permanent phone suspensions.

## Architecture & Code Pattern

```python
import random

GREETINGS = [
    "Hi {name}!",
    "Hello {name} team,",
    "Hey {name}!",
    "Good day {name} team,"
]

HOOKS_NICHE = {
    "auto": [
        "I came across your business on Google Maps in {city} and was really impressed by your stellar {rating}★ rating and customer reviews.",
        "Saw your profile on Google Maps while looking at top-rated auto services in {city} — amazing {rating}★ feedback from your customers.",
        "Found your service listing on Google Maps in {city}. Your {rating}★ reputation really stands out in the area.",
        "I was checking out highly-rated local businesses in {city} on Google Maps and noticed your excellent {rating}★ rating."
    ],
    "medical": [
        "I found your practice on Google Maps in {city} with an impressive {rating}★ rating and great patient feedback.",
        "Came across your clinic listing on Google Maps in {city} — your {rating}★ patient reviews really caught my attention."
    ],
    "home_services": [
        "I noticed your listing on Google Maps in {city} with an outstanding {rating}★ rating and great reviews.",
        "Found your business on Google Maps in {city} — great to see your solid {rating}★ customer feedback in the local area."
    ]
}

PAIN_POINTS = [
    "I noticed you don't currently have an official website or automated booking system linked to your listing, which means potential customers might be turning to competitors who offer 24/7 online booking.",
    "I saw you don't have a direct website attached to your Google Maps profile yet. Without online scheduling, valuable high-ticket clients often end up booking with other businesses that accept instant requests.",
    "Looking at your profile, you don't currently have a dedicated website or instant quote system. In {city}, many clients look to book appointments online after hours rather than calling.",
    "I noticed your Google Maps listing doesn't link to a direct website. Many customers searching for {niche} prefer booking online instantly, so missing a web page often means leaving revenue on the table."
]

VALUE_PROPS = [
    "At Avalanche Agency, we build high-converting websites equipped with 24/7 AI Receptionists that automatically answer inquiries and schedule bookings directly into your calendar in under 48 hours ($490).",
    "We help local businesses set up custom, mobile-first websites with built-in AI Booking Assistants that capture leads and lock in appointments around the clock in just 48h ($490 flat).",
    "At Avalanche Agency, we craft sleek websites integrated with smart 24/7 AI Sales Assistants that handle client questions and schedule appointments 24/7, delivered in 48 hours ($490)."
]

CTAS = [
    "Would you be open to seeing a quick 2-minute live concept customized for {name}?",
    "Could I send over a quick 2-minute interactive demo tailored for your team?",
    "Would you be interested in checking out a quick 2-minute preview designed for {name}?",
    "Happy to share a quick 2-minute live preview if you'd like to see how it works for {name}?"
]

SIGN_OFFS = [
    "Best regards,\nBen Jett | Avalanche Agency\nhttps://aavalanche.com",
    "Best,\nBen Jett | Avalanche Agency\nhttps://aavalanche.com",
    "Warm regards,\nBen Jett\nAvalanche Agency & Enlight Group\nhttps://aavalanche.com"
]

def generate_varied_pitch(name, city, niche, rating):
    greeting = random.choice(GREETINGS).format(name=name)
    hook_list = HOOKS_NICHE.get(niche.lower(), HOOKS_NICHE["home_services"])
    hook = random.choice(hook_list).format(name=name, city=city, rating=rating)
    pain = random.choice(PAIN_POINTS).format(name=name, city=city, niche=niche)
    value = random.choice(VALUE_PROPS)
    cta = random.choice(CTAS).format(name=name)
    sign_off = random.choice(SIGN_OFFS)
    return f"{greeting}\n\n{hook}\n\n{pain}\n\n{value}\n\n{cta}\n\n{sign_off}"
```

## Key Rules
1. **Never use static copy:** Every lead receives a unique combination of sentences.
2. **Pre-dispatch Validation:** Check `len(pitch) >= 50` and ensure no `Custom pitch` or placeholder phrases exist.
3. **Clean Root Links:** Default signature links to the top-level agency website (`https://aavalanche.com`).
