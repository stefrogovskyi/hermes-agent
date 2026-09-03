import re

title = "How to Build a Long-Term Logistics Career"
meta_title = "How to Build a Long-Term Logistics Career"
meta_description = "Update your resume, master shipping technology, earn industry certifications, and build professional networks to maintain career stability in logistics."

body = """
Global market shifts and evolving shipping technologies alter logistics operations every year. Staying competitive across a long career requires active adjustments to how you track tools, update qualifications, and respond to industry disruptions.

## Maintaining an Active Resume

A resume saved on a hard drive quickly grows outdated. Hiring a resume writing service can refresh your documentation, even if you are not currently looking for a new position. 

Sudden disruptions like the COVID-19 pandemic, natural disasters, or human conflicts can trigger economic shocks, corporate closures, and layoffs. Keeping an updated resume ensures readiness if an unexpected job search occurs. Current resumes are also required when applying for internal promotions or reviewing whether existing wages and benefits align with market standards.

## Adapting to Technological Shifts

Company cultures vary between innovative adoption and traditional routines. Hardware reaches the end of its operational lifespan, and software vendor support ends once tools lose utility. Digital obsolescence forces teams to adopt updated software, though early implementation helps improve operational efficiency.

Logistics professionals monitor several specific tools:

* Blockchain provides immutable data storage where recorded information cannot be changed. This transparency traces products from origin to consumer, enabling real-time shipment tracking and process automation.
* Robotics introduces new forms of automation inside warehouses and distribution centers.
* Data analytics software replaces manual spreadsheets and gut feelings by visualizing real-time tracking data and shipping insights. These visual tools inform operational decision-making, optimize logistics workflows, and enhance supply chain efficiency.

## Pursuing Continuous Education

Maintaining relevant terminology as new jargon enters the field requires ongoing learning. Reading industry publications keeps you informed of shifting terminology. Participating in conventions, conferences, seminars, trade shows, workshops, and webinars connects technical concepts to operational practice.

Formal education options include online classes, employer-sponsored training, and education stipends. Professional certifications build specialized knowledge in blockchain technology, robotic process automation (RPA), and the Internet of Things (IoT). Industry credentials like the Certified Supply Chain Professional (CSCP) and Certified in Logistics, Transportation, and Distribution (CLTD) demonstrate verified expertise. 

For those holding a bachelor's degree in Supply Chain Management, Business Management, or related fields, pursuing an MBA focused on logistics or a Master's degree in Supply Chain Management expands career knowledge and opens lucrative positions.

## Building Professional Networks

Attending industry events and classes provides opportunities to connect with peers. Following up with new contacts on LinkedIn keeps those professional relationships active. 

Joining industry associations offers structured engagement. Organizations like the Institute for Supply Management (ISM) and the Counsel of Supply Chain Management Professionals (CSCMP) offer direct access to broader professional networks.

## Developing Operational Flexibility

In science fiction, a conquering alien species stays effective by adapting quickly to changing circumstances. Developing a similar level of flexibility protects your career as new techniques replace old habits.

Cultivating a growth mindset helps you treat operational challenges as learning opportunities instead of setbacks. Regular practice in troubleshooting and problem-solving builds the practical resilience needed to manage freight calculation updates, CO2 footprint reduction requirements, and shifting supply chain demands. Keeping your resume current records these professional achievements as your career moves forward.
"""

def full_check(title, meta_title, meta_desc, body):
    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"
    print("=== FULL VERIFICATION REPORT ===")
    
    # Rule 1: Forbidden dashes
    # Rule specifies: (em-dash —, en-dash –, double hyphen --)
    forbidden_dashes = ['—', '–', '--']
    found_dashes = [d for d in forbidden_dashes if d in full_text]
    print(f"Rule 1 (Forbidden dashes —, –, --): {'PASS (0 found)' if not found_dashes else f'FAIL ({found_dashes})'}")
    
    # Let's also check standard hyphen count / presence just to be aware
    print(f"Standard hyphens count: {full_text.count('-')}")

    # Rule 2: Metaphor count
    # Let's count metaphors manually or list potential ones:
    # Metaphor in text: "conquering alien species" (analogy/reference from text), any others?
    # Original text had: "dusty old resume", "Stone Age", "conquering alien species".
    # In our draft: no "dusty old resume", no "Stone Age". Only the sci-fi alien reference.
    
    # Rule 3: Textbook architecture & cliché transitions
    cliches = ["in conclusion", "as we have seen", "furthermore", "moreover", "let's dive into", "to sum up", "firstly", "secondly", "finally"]
    found_cliches = [c for c in cliches if re.search(r'\b' + re.escape(c) + r'\b', full_text, re.I)]
    print(f"Rule 3 (Cliché transitions): {'PASS (None found)' if not found_cliches else f'FAIL ({found_cliches})'}")

    # Rule 4: Zero explicit connectors
    connectors = ["that's why", "this is because", "as a result", "consequently"]
    found_conn = [c for c in connectors if re.search(r'\b' + re.escape(c) + r'\b', full_text, re.I)]
    print(f"Rule 4 (Forced connectors): {'PASS (None found)' if not found_conn else f'FAIL ({found_conn})'}")

    # Rule 5: Contrastive negation limit (max 1 instance of "X, not Y", "rather than", "instead of")
    cn_phrases = ["rather than", "instead of"]
    found_cn = re.findall(r'\b(rather than|instead of)\b', full_text, re.I)
    # Also search for ", not "
    comma_not = re.findall(r',\s*not\b', full_text, re.I)
    print(f"Rule 5 (Contrastive negation): found 'rather than/instead of': {found_cn}, found ', not ': {comma_not}. Total count: {len(found_cn) + len(comma_not)} (Max allowed: 1)")

    # Rule 6: Single sentence paragraphs (aphoristic)
    lines = [p.strip() for p in body.split('\n') if p.strip() and not p.strip().startswith('#') and not p.strip().startswith('*')]
    single_sentence_paras = []
    for p in lines:
        # count sentences in paragraph
        sentences = [s for s in re.split(r'[.!?]+', p) if s.strip()]
        if len(sentences) == 1:
            single_sentence_paras.append(p)
    print(f"Rule 6 (Single-sentence paragraphs): {len(single_sentence_paras)} found.")
    for ssp in single_sentence_paras:
        print(f"  -> Single sentence para: '{ssp}'")

    # Rule 9: Banned AI vocabulary
    banned_words = [
        "delve", "tapestry", "beacon", "testament", "crucial", "pivotal",
        "game-changer", "seamless", "ever-evolving", "paramount", "foster",
        "unlock", "harness", "empower", "spearhead", "robust", "demystify",
        "revolutionize", "cutting-edge", "realm"
    ]
    found_banned = [w for w in banned_words if re.search(r'\b' + re.escape(w) + r'\b', full_text, re.I)]
    print(f"Rule 9 (Banned AI words): {'PASS (None found)' if not found_banned else f'FAIL ({found_banned})'}")

    # Rule 10: Character limits
    print(f"Rule 10 (Length limits):")
    print(f"  H1 Title: {len(title)} chars (max 60) -> {'PASS' if len(title) <= 60 else 'FAIL'}")
    print(f"  Meta Title: {len(meta_title)} chars (max 60) -> {'PASS' if len(meta_title) <= 60 else 'FAIL'}")
    print(f"  Meta Description: {len(meta_desc)} chars (max 155) -> {'PASS' if len(meta_desc) <= 155 else 'FAIL'}")

full_check(title, meta_title, meta_description, body)
