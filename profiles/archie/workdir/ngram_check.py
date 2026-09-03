import re

original = """
Shipping teams are dealing with a different kind of problem now. It is not just about cost and transit time anymore. A route that looks workable one week can get more expensive, slower, or less reliable the next because of tariffs, port congestion, political tension, or capacity changes somewhere upstream.

That is why "smart shipping" means something more concrete than it used to. It means reading the market early, spreading risk where it makes sense, and building enough flexibility into routing and capacity decisions that one disruption does not throw everything off at once.

Good shipping decisions now tend to rest on three things working together: market awareness, diversified capacity, and backup routing that is thought through before anyone needs it. If one of those is missing, the whole setup gets more fragile.

Market awareness means watching where freight conditions are heading before that shows up in a booking quote. Diversified capacity means not being too dependent on one carrier, one trade lane, or one sourcing origin. Scenario-based routing means alternatives already exist on paper before disruption makes them urgent.

That matters more now because the trade environment punishes concentration faster than it used to. Tariffs, geopolitical tension, and uneven container flows have made single-point dependence expensive. Speed still matters. Cost still matters. Resilience does too. The real job is keeping them in balance.

This same logic applies beyond shipping. Firms that manage risk well tend to spread exposure across multiple options rather than concentrating it, whether across suppliers, carriers, and shipping corridors, or across asset classes. The principle is the same across industries: avoid putting everything in one place.

Freight markets move on information, and shippers who wait for rate confirmations before acting are already behind. The gap between reactive and strategic procurement often comes down to one thing: when a team starts reading the market relative to when they book.

Not all market data is equally useful when it is time to make a booking decision. Rates get the most attention because they are visible, but they are often late. By the time a higher number shows up on a quote, the pressure behind it has usually been building for a while.

The earlier clues tend to be structural: blank sailings, worsening port congestion, carrier capacity changes, and shifts in trade policy. OECD shipping research has shown how disruption in major container corridors can trigger knock-on effects in both rates and available capacity before those changes are fully visible in market pricing.

Looking at those signals together gives procurement teams a better sense of where the market is headed, not just what it happens to look like today.

Reading signals well is only useful when it changes what gets booked, when, and under what terms. The broader principle is the same in any fast-moving market: better decisions usually come from acting on structured signals before conditions fully shift.

Real-time visibility plays a direct role here. Teams using live shipment data alongside market indicators can intervene earlier, adjusting routing or carrier selection before conditions fully shift rather than scrambling after the fact.

This is where scenario planning and risk mitigation become operational rather than theoretical. The goal isn't predicting the market perfectly. It's building enough lead time to act before options narrow.

Supply chain diversification is often understood too narrowly. Adding a second supplier in the same country or with the same carrier doesn't meaningfully reduce exposure. It just creates the appearance of optionality. Real diversification requires looking at where capacity is actually concentrated and separating those risks across geographies, providers, and corridors.

Sourcing across more than one country used to sound like a contingency plan. Now it looks a lot more like standard risk management. The China-plus-one model captures that shift pretty well, with companies spreading production across India, Vietnam, Mexico, and other ASEAN markets instead of leaving too much riding on one manufacturing base.

Each one comes with a different set of trade-offs. Vietnam continues to look strong in electronics and apparel because the manufacturing economics still work and the export infrastructure keeps getting better. India offers scale and improving logistics, which matters a lot in pharmaceutical and industrial goods. Mexico changes the equation in a different way, especially for North American supply chains, because proximity helps with both transit time and tariff exposure.

Southeast Asia has taken on a good share of this shift in recent years. Some of it came from tariff pressure. Some of it came from companies stress-testing how much risk they were carrying in a single-origin setup. The broader effect is pretty clear: a more distributed footprint and less damage when one origin gets disrupted.

Diversifying sourcing only solves one part of the problem. Carrier concentration and route concentration create their own kind of exposure, and a lot of shippers do not really feel that until something goes wrong. If too much volume sits with one alliance or one corridor, a single disruption can throw off the whole plan.

The Red Sea disruption made that pretty obvious. Once that route became less reliable, cargo started shifting away from the Suez Canal and onto the longer Cape of Good Hope route. That added time, pushed pressure into Europe-bound lanes, and tightened capacity where shippers were already feeling stretched.

That is why spreading volume across multiple carriers matters. So does knowing the alternate corridors before you need them. If those options are already familiar, a disruption is still a problem, but it is not a blind scramble.

Diversification does protect you, but it also adds friction. More carriers, more sourcing locations, more routing options, each one sounds like flexibility on paper, but in practice it means more moving parts to stay on top of. That workload builds quickly once volume scales.

Each additional supplier relationship requires onboarding, compliance documentation, and ongoing performance monitoring. Each new corridor adds rate tracking and operational oversight. These aren't reasons to avoid diversification. They're costs that need to be weighed honestly against the supply chain resilience gains they produce.

The clearest trade-off involves volume concentration. Consolidating freight with fewer carriers typically unlocks better contract rates and priority capacity access. Splitting volume for risk mitigation purposes reduces that positioning, and the rate difference can be material depending on corridor and commodity type.

Duplicated compliance work is another real cost, particularly when sourcing shifts involve new trade agreements, tariff classifications, or country-of-origin documentation requirements. Trade policy changes don't simplify that burden. They often accelerate it.

The practical question is not "should we diversify?" but "where does it actually pay off?" Some lanes justify the extra effort. Others do not. High-margin, business-critical components with volatile demand and tariff exposure usually earn that investment. Low-risk, easily replaceable inputs often do not. That is why the better approach is targeted, not blanket.

Scenario planning helps prioritize where to invest in optionality. By mapping lanes and suppliers against margin, criticality, and disruption probability, supply chain teams can concentrate resilience spending where it produces the most protection, rather than applying it uniformly and absorbing unnecessary overhead across the board.

A playbook is what turns strategy into something usable when the market gets messy. The teams that respond well usually are not inventing their response in real time. They have already decided what certain disruptions mean and what happens next when those conditions show up.

That starts with triggers. If rates on a core lane jump past a set threshold, the playbook should already say whether the move is to shift into spot, activate another carrier, or reroute. If tariffs change or geopolitical pressure builds around a key corridor, the fallback options should already be sitting there, not waiting to be figured out in the middle of the problem.

Scenario planning is what makes those trigger points useful instead of theoretical. If a team has already worked through the cost and timing impact of a Red Sea-style closure, a carrier alliance shakeup, or a sudden tariff move, they are not starting cold when something shifts.

Real-time visibility matters because it tells you when the trigger has actually been hit. Shared ownership matters too. Procurement, logistics, finance, and trade compliance all need to be working from the same definitions of what counts as a trigger and who is expected to act.

The point is not to build a playbook for every imaginable crisis. It is to create a decision structure that holds up across different kinds of disruption, so the response is faster and a lot less improvised.

Smart shipping isn't about building the most elaborate supply chain structure. It's about reducing exposure where it matters most and staying capable of responding when conditions shift.

The strategies covered throughout this article share a common thread: combining market insight with targeted supply chain diversification produces better decisions than optimizing any single variable in isolation. Freight rates, carrier relationships, sourcing geographies, and routing alternatives all interact, and understanding those interactions is what creates real supply chain resilience.

The practical takeaway is a principle rather than a checklist. Identify where concentration risk is highest across lanes, carriers, and origins. Prioritize resilience investment there, not uniformly across every product and corridor. Monitor container trade signals early enough to act before options narrow.

Complexity isn't the goal. Optionality is. The more a supply chain team can respond to changing freight conditions without scrambling to build new relationships or reroute from scratch, the more effectively they can protect margins and maintain service commitments when the market moves against them.
"""

with open('searates_final_v3.md', encoding='utf-8') as f:
    content = f.read()
body = content.split('# BODY')[1].strip()

def normalize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s']", ' ', text)
    return text.split()

def ngrams(words, n=6):
    return set(tuple(words[i:i+n]) for i in range(len(words)-n+1))

orig_words = normalize(original)
body_words = normalize(body)

orig_6 = ngrams(orig_words, 6)
body_6 = ngrams(body_words, 6)

overlap = orig_6.intersection(body_6)
print("6-gram overlap count:", len(overlap))
for g in sorted(overlap):
    print(' '.join(g))
