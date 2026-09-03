import re

source_text = """Thank you for your continued support of SeaRates. We are pleased to present new solutions and improvements that better meet your needs in trading and logistics. We are continuing to lay a significant emphasis on the enhancement of our services.

What’s new for week 8:

Terminal API Version 1.0:
From now on, you can access data from 17,000+ terminals by SMDG and BIC codes.
Ensure smooth and global terminal data gathering with added support for CONTAINER TERMINAL ODESSA (CTO) and BROOKLYN-KIEV PORT (BKP), as well as for the following container statuses: UNKNOWN, ON_TERMINAL, NOT_ON_TERMINAL, TERMINAL_NOT_SUPPORTED, TERMINAL_NO_RESPONSE, UNEXPECTED_ERROR.

Tracking System updates:
We are pleased to announce added support for 3 more shipping lines, namely GS Lines, Bahri (Saudi Arabia), and Vuxx Shipping, bringing the total number to 191.
Also, we have made enhancements to our collaboration with shipping lines, including Gold Star Line, Crane Worldwide Logistics, Dong Young, White Line Shipping, Hede Shipping, Dole Ocean Cargo Express, Matson Navigation, Aladin Express, Namsung Shipping, Maersk, Mediterranean Shipping Company (MSC), CMA CGM, American President Lines (APL), CNC (Cheng Lie Navigation), and Australia National Line (ANL).

Ship Schedules enhancements:
We have improved our support for providers, namely for ONE, Hapag-Lloyd, Wan Hai, Yang Ming, and Sinotrans by Points.

Other updates:
For the Bookings, we have implemented route displaying by shipment and delivery type under 'Details' tab."""

draft_text = """Title: SeaRates Week 8 Updates: Terminal API, Carrier Tracking
Meta-Title: SeaRates 2025 Week 8: Terminal API and Carrier Tracking
Meta-Description: SeaRates launches Terminal API v1.0, adds 3 carriers for multi-carrier tracking, updates ocean freight visibility tools, and refines ship schedules.

Body Text:
SeaRates released several platform updates in Week 8 of 2025 across terminal data, vessel tracking, sailing schedules, and booking management.

Terminal API integration reached Version 1.0, opening access to data across more than 17,000 facilities indexed by SMDG and BIC codes. The update adds support for CONTAINER TERMINAL ODESSA (CTO) alongside BROOKLYN-KIEV PORT (BKP). Raw status responses now return specific facility flags. These include UNKNOWN, ON_TERMINAL, NOT_ON_TERMINAL, TERMINAL_NOT_SUPPORTED, TERMINAL_NO_RESPONSE, plus UNEXPECTED_ERROR. Standardizing these codes gives logistics teams cleaner container status tracking during terminal handoffs.

Multi-carrier tracking expanded to 191 supported ocean lines. GS Lines and Bahri (Saudi Arabia) joined the platform, alongside Vuxx Shipping. Data connections were also refined across fifteen established shipping lines. Ocean freight visibility improves through updated carrier feeds from Gold Star Line, Crane Worldwide Logistics, Dong Young, White Line Shipping, Hede Shipping, Dole Ocean Cargo Express, Matson Navigation, Aladin Express, Namsung Shipping, Maersk, Mediterranean Shipping Company (MSC), CMA CGM, American President Lines (APL), CNC (Cheng Lie Navigation), and Australia National Line (ANL).

Ship Schedules logic was updated for query results by Points across five providers: ONE, Hapag-Lloyd, Wan Hai, Yang Ming, and Sinotrans. Separately, booking management interfaces now display route details organized by shipment type and delivery mode within the Details tab."""

def get_words(text):
    return re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())

s_words = get_words(source_text)
d_words = get_words(draft_text)

s_full = " ".join(s_words)

for i in range(len(d_words) - 5):
    gram = d_words[i:i+6]
    gram_str = " ".join(gram)
    if gram_str in s_full:
        print(f"Match at draft index {i}: '{gram_str}'")

