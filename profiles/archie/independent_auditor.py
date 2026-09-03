import re
import test_full_draft_v3

original_text = """Our industry is known for its complexity and rapid pace of development, where changes can take you by surprise. The world of logistics has seen tangible shifts — a surge in the interest in artificial intelligence. It is hard to ignore the prospects from digital agents to automated pricing tools. Despite the excitement, one thing remains the same: logistics is a sector in which people and their professionalism play a major role.

The true power of artificial intelligence and machine learning is not to replace people, but to enable them to work smarter and more efficiently. It is a delicate balance between technology and experience that requires us to evolve with these new tools.

Aleksey Shatunov, co-founder of SeaRates, shared his thoughts regarding this point:

"Caught up with a bunch of old mates this week — folks from shipping lines and top-tier freight forwarding companies. Almost all of them were genuinely excited about AI. From digital agents to automated pricing and planning tools — the buzz is real.

But here’s the catch:

Logistics is still a bit of an old dog — slow to adapt, set in its ways.

And we, the experienced logisticians, often find ourselves chasing the trend instead of shaping it.

I’ve heard countless stories lately where companies fired people too soon, thinking AI would replace them — only to realize they had to hire back, this time for new hybrid roles.

The point is — it’s not about losing your job. It’s about evolving with it.

And let’s be honest — no AI can (yet) explain to a stressed-out customer why their container missed the transhipment and now the factory’s on standby for raw materials. That takes context, empathy, and experience.

Don’t worry — AI’s not taking your job. But it might just need your help to do its job. 😉

P.S.: At SeaRates.com, we always know where your goods are. Be it by sea, rail, road… or doing 600mph over the Atlantic."

You are always welcome to contribute to the development of the logistics industry and solve your daily challenges by contacting our team at SeaRates."""

rewrite_text = test_full_draft_v3.body

print("--- AUDITOR PASS: SIMILARITY CHECK ---")
# Check 6+ consecutive word overlap (excluding standard terms or quotes)
def get_ngrams(text, n=6):
    words = re.findall(r'\b\w+\b', text.lower())
    return set([' '.join(words[i:i+n]) for i in range(len(words)-n+1)])

orig_ngrams = get_ngrams(original_text)
rewrite_ngrams = get_ngrams(rewrite_text)

# Exclude quote words since quote is preserved
quote_ngrams = get_ngrams(original_text[original_text.find('"'):original_text.rfind('"')+1])

overlaps = (orig_ngrams & rewrite_ngrams) - quote_ngrams
print(f"Non-quote 6-gram overlaps found: {len(overlaps)}")
for ov in overlaps:
    print("  - Overlap:", ov)

print("AUDITOR PASS COMPLETE.")
