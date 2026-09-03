import re
import json

title = "How to Build a Long-Term Logistics Career"
meta_title = "How to Build a Long-Term Logistics Career"
meta_desc = "Update your resume, master shipping technology, earn industry certifications, and build professional networks to maintain career stability in logistics."

body_text = """Shifting global trade flows and continuous technological upgrades in shipping alter freight operations every year. Staying competitive across a long career requires active adjustments to how you track tools, update qualifications, and respond to industry disruptions.

## Maintaining an Active Resume

A resume saved on a hard drive quickly grows outdated. Hiring a resume writing service can refresh your documentation, even if you do not currently plan to change jobs.

Major disruptions such as regional conflicts, severe weather events, or global health crises like the COVID-19 outbreak trigger sudden economic shocks, corporate closures, and layoffs. Keeping an updated resume ensures readiness if an unexpected job search occurs. Current resumes are also required when applying for internal promotions or reviewing whether existing wages and benefits align with market standards.

## Adapting to Technological Shifts

Company cultures vary between innovative adoption and traditional routines. Hardware reaches the end of its operational lifespan, and software vendor support ends once tools lose utility. Digital obsolescence forces teams to adopt updated software, though early implementation helps improve operational efficiency.

Logistics professionals monitor several specific tools to maintain operational efficiency. Blockchain provides immutable data storage where recorded information cannot be changed, tracing products from origin to consumer to enable real-time shipment tracking and process automation. Robotics introduces new forms of automation inside warehouses and fulfillment hubs. Data analytics software replaces manual spreadsheets and gut feelings by visualizing real-time tracking data and shipping insights, guiding operational decisions and enhancing supply chain efficiency.

## Pursuing Continuous Education

Keeping pace as industry vocabulary shifts alongside technological adoption requires ongoing learning. Reading trade publications helps you stay informed of emerging terminology. You can also participate in industry summits, commercial expos, specialized workshops, and online webinars to connect technical concepts with daily operational practice.

Formal education options include online classes, employer-sponsored training, and tuition stipends. Professional certifications build specialized knowledge in blockchain technology, robotic process automation (RPA), and the Internet of Things (IoT). Industry credentials like the Certified Supply Chain Professional (CSCP) and Certified in Logistics, Transportation, and Distribution (CLTD) demonstrate verified expertise. For professionals holding an undergraduate degree in business or supply chain management, earning an MBA focused on logistics or a graduate degree in supply chain management expands career knowledge and opens lucrative positions.

## Building Professional Networks

Industry conventions and classes offer prime opportunities to connect with peers. Reaching out to new acquaintances on LinkedIn keeps those professional relationships active over time.

Joining trade associations provides structured engagement. Organizations like the Institute for Supply Management (ISM) and the Counsel of Supply Chain Management Professionals (CSCMP) offer direct access to broader professional networks.

## Developing Operational Flexibility

In science fiction, a conquering alien species stays effective by adapting quickly to changing circumstances. Developing a similar level of flexibility protects your career as new techniques replace old habits.

Cultivating a growth mindset helps you treat operational challenges as learning opportunities instead of setbacks. Regular practice in troubleshooting and problem-solving builds the practical resilience needed to manage freight calculation updates, CO2 footprint reduction requirements, and shifting supply chain demands. Keeping your resume current records these professional achievements as your career moves forward."""

def get_ngrams(text, n=6):
    words = re.findall(r'\b[a-z0-9]+\b', text.lower())
    return set(" ".join(words[i:i+n]) for i in range(len(words)-n+1))

with open("/opt/hermes/profiles/archie/original_article.txt", "r", encoding="utf-8") as f:
    orig_text = f.read()

orig_ngrams = get_ngrams(orig_text, 6)
rewrite_ngrams = get_ngrams(body_text, 6)

overlap = orig_ngrams.intersection(rewrite_ngrams)

# Exclude trade terms/names if any
trade_terms = [
    "supply chain management", "certified supply chain professional",
    "certified in logistics transportation and", "logistics transportation and distribution",
    "institute for supply management", "counsel of supply chain management professionals",
    "internet of things", "robotic process automation", "real time tracking data"
]

filtered_overlap = [ng for ng in overlap if not any(tt in ng for tt in trade_terms)]

print("=== CHECK RESULTS ===")
print("Title Length:", len(title), "chars")
print("Meta Title Length:", len(meta_title), "chars")
print("Meta Desc Length:", len(meta_desc), "chars")

# Check dashes
dashes = re.findall(r'[—–]|--', title + meta_title + meta_desc + body_text)
print("Forbidden dashes found:", len(dashes), dashes)

# Check contrastive negations
cn_matches = re.findall(r'\b(instead of|rather than|not [a-z]+ but|not only [a-z]+ but)\b', body_text, re.IGNORECASE)
print("Contrastive negations count:", len(cn_matches), cn_matches)

# Check banned AI words
banned_words = ["delve", "tapestry", "beacon", "testament", "crucial", "pivotal", "game-changer", "seamless", "ever-evolving", "paramount", "foster", "unlock", "harness", "empower", "spearhead", "robust", "demystify", "revolutionize", "cutting-edge", "realm"]
found_banned = [w for w in banned_words if re.search(rf'\b{w}\b', body_text, re.IGNORECASE)]
print("Banned AI words found:", len(found_banned), found_banned)

print("6-gram Overlaps total:", len(overlap))
print("Filtered 6-gram Overlaps (excl. trade terms):", len(filtered_overlap), filtered_overlap)

with open("/opt/hermes/profiles/archie/final_article.json", "w", encoding="utf-8") as f:
    json.dump({
        "title": title,
        "meta_title": meta_title,
        "meta_description": meta_desc,
        "body": body_text
    }, f, ensure_ascii=False, indent=2)
