import re, sys
f = "/opt/hermes/profiles/archie/workdir/weekly_digest_jun8_15_rewrite.md"
t = open(f).read()
print("em-dash:", t.count("\u2014"), "| double-hyphen:", t.count("--"))
for m in re.finditer(r"\b(not|instead of|that's why|which is why|it's not)\b", t, re.I):
    print("TELL:", m.group(0), "->", t[max(0,m.start()-60):m.end()+60].replace("\n"," "))
def ngrams(s, n=6):
    w = re.findall(r"[a-z0-9']+", s.lower())
    return {' '.join(w[i:i+n]) for i in range(len(w)-n+1)}
src = """MSC is reportedly restructuring parts of its South Asia service carrier network and changing hub operations across regional trade lanes. India Sri Lanka Bangladesh transit times transshipment points vessel connections schedule reliability booking decisions cut-off planning expected arrival windows downstream delays Vessel monitoring departures routing path intermediate ports connection reliability port congestion North Europe East Asia late departures berth availability rolled cargo missed cut-offs longer transit times demurrage detention real-time container tracking live delay alerts Georgia Ports Authority Ocean Terminal Savannah 55% complete cargo handling mixed cargo flows peak periods US East Coast routing options port selection customs enforcement inspections counterfeit non-compliant goods customs holds documentation reviews cargo release delays container location vessel movement port congestion schedule reliability transshipment delays customs holds release status predictive ETA risk alerts inland delivery milestones SeaRates Tracking System sales@searates.com"""
ov = ngrams(t) & ngrams(src)
print("6-gram overlap vs source fact-sheet:", len(ov))
for g in sorted(ov): print("  ", g)
wc = len(re.findall(r"\b\w+\b", t)); print("word count:", wc)
