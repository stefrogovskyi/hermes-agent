import random

GREETINGS = [
    "Hi {name}!",
    "Hello {name} team,",
    "Hey {name}!",
    "Good day {name} team,"
]

# For rating >= 4.0
HOOKS_HIGH_RATING = [
    "I came across your business on Google Maps in {city} and was really impressed by your {rating}★ rating and customer reviews.",
    "Saw your profile on Google Maps while looking at top-rated local services in {city} — amazing {rating}★ feedback from your clients.",
    "Found your service listing on Google Maps in {city}. Your strong {rating}★ reputation really stands out in the area.",
    "I was checking out highly-rated local businesses in {city} on Google Maps and noticed your excellent {rating}★ rating."
]

# For rating < 4.0 (Reputation Growth & Review Recovery Angle)
HOOKS_LOW_RATING = [
    "I came across your business listing on Google Maps in {city}. I noticed you currently have a {rating}★ rating and some mixed feedback from past clients.",
    "Saw your business profile on Google Maps in {city}. While you offer great services, your public {rating}★ rating might be costing you new clients to local competitors.",
    "Found your service profile on Google Maps in {city} ({rating}★). Many local service businesses struggle with unmanaged Google reviews that don't reflect their true quality of work.",
    "I was researching service providers in {city} on Google Maps and noticed your {rating}★ profile. In competitive markets, public ratings heavily influence customer trust."
]

PAIN_HIGH_RATING = [
    "I noticed you don't currently have an official website or automated booking system linked to your listing, which means potential customers might be turning to competitors who offer 24/7 online booking.",
    "I saw you don't have a direct website attached to your Google Maps profile yet. Without online scheduling, valuable high-ticket clients often end up booking with other businesses that accept instant requests.",
    "Looking at your profile, you don't currently have a dedicated website or instant quote system. In {city}, many clients look to book appointments online after hours rather than calling.",
    "I noticed your Google Maps listing doesn't link to a direct website. Many customers searching for {niche} prefer booking online instantly, so missing a web page often means leaving revenue on the table."
]

PAIN_LOW_RATING = [
    "Without a direct website and an automated feedback filter, dissatisfied customers go straight to Google Maps to leave negative reviews instead of resolving issues privately with you.",
    "Not having an official website with a smart review-generation system means you're missing out on collecting 5-star reviews from happy clients to push your rating back up to 4.8★+.",
    "Competitors with 4.8★+ profiles and instant booking websites are winning the majority of local search traffic, but a dedicated reputation funnel can quickly turn this around.",
    "Relying solely on Google Maps without an official website prevents you from controlling your brand story and automatically collecting positive customer feedback."
]

VALUE_HIGH_RATING = [
    "At Avalanche Agency, we build high-converting websites equipped with 24/7 AI Receptionists that automatically answer inquiries and schedule bookings directly into your calendar in under 48 hours ($490).",
    "We help local businesses set up custom, mobile-first websites with built-in AI Booking Assistants that capture leads and lock in appointments around the clock in just 48h ($490 flat).",
    "At Avalanche Agency, we craft sleek websites integrated with smart 24/7 AI Sales Assistants that handle client questions and schedule appointments 24/7, delivered in 48 hours ($490).",
    "We specialize in rapid 48-hour turnarounds ($490) building modern websites with 24/7 AI assistants that convert Google Maps traffic into confirmed appointments automatically."
]

VALUE_LOW_RATING = [
    "At Avalanche Agency, we build modern websites equipped with 24/7 AI Receptionists and built-in Smart Review Funnels that automatically boost your Google rating while booking new clients in 48h ($490).",
    "We build custom landing pages ($490 in 48h) with integrated AI Assistants that route customer feedback privately to you and automatically invite happy customers to leave 5★ Google reviews.",
    "We help local businesses rebuild their digital reputation: high-converting websites + 24/7 AI Assistants that capture direct bookings and run automated 5-star review campaigns ($490).",
    "At Avalanche Agency, we create 48-hour turnkey solutions ($490) combining a fast mobile website, 24/7 AI booking, and an automated reputation system to raise your Google rating."
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

def generate_varied_pitch(name, city, niche, rating_str):
    greeting = random.choice(GREETINGS).format(name=name)
    
    try:
        r_val = float(rating_str)
    except Exception:
        r_val = 4.5
        
    if r_val < 4.0 and r_val > 0:
        hook = random.choice(HOOKS_LOW_RATING).format(name=name, city=city, rating=rating_str, niche=niche)
        pain = random.choice(PAIN_LOW_RATING).format(name=name, city=city, niche=niche)
        value = random.choice(VALUE_LOW_RATING)
    else:
        hook = random.choice(HOOKS_HIGH_RATING).format(name=name, city=city, rating=rating_str, niche=niche)
        pain = random.choice(PAIN_HIGH_RATING).format(name=name, city=city, niche=niche)
        value = random.choice(VALUE_HIGH_RATING)
        
    cta = random.choice(CTAS).format(name=name)
    sign_off = random.choice(SIGN_OFFS)
    
    return f"{greeting}\n\n{hook}\n\n{pain}\n\n{value}\n\n{cta}\n\n{sign_off}"

if __name__ == "__main__":
    print("=== HIGH RATING SAMPLE ===")
    print(generate_varied_pitch("Miami Collision Pro", "Miami, FL", "Auto Repair", "4.8"))
    print("\n=== LOW RATING SAMPLE (< 4.0) ===")
    print(generate_varied_pitch("Express Towing & Tires", "Orlando, FL", "Towing & Tires", "3.4"))
