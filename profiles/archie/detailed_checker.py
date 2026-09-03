import re

title = "How to Build a Long-Term Logistics Career"
meta_title = "How to Build a Long-Term Logistics Career"
meta_desc = "Update your resume, master shipping technology, earn industry certifications, and build professional networks to maintain career stability in logistics."

body = """
Global market shifts and evolving shipping technologies alter logistics operations every year. Staying competitive across a long career requires active adjustments to how you track tools, update qualifications, and respond to industry disruptions.

## Maintaining an Active Resume

A resume saved on a hard drive quickly grows outdated. Hiring a resume writing service can refresh your documentation, even if you do not currently plan to change jobs.

Sudden disruptions like the COVID-19 pandemic, natural disasters, or human conflicts can trigger economic shocks, corporate closures, and layoffs. Keeping an updated resume ensures readiness if an unexpected job search occurs. Current resumes are also required when applying for internal promotions or reviewing whether existing wages and benefits align with market standards.

## Adapting to Technological Shifts

Company cultures vary between innovative adoption and traditional routines. Hardware reaches the end of its operational lifespan, and software vendor support ends once tools lose utility. Digital obsolescence forces teams to adopt updated software, though early implementation helps improve operational efficiency.

Logistics professionals monitor several specific tools to maintain operational visibility:

* Blockchain provides immutable data storage where recorded information cannot be changed. This transparency traces products from origin to consumer, enabling real-time shipment tracking and process automation.
* Robotics introduces new forms of automation inside warehouses and distribution centers.
* Data analytics software replaces manual spreadsheets and gut feelings by visualizing real-time tracking data and shipping insights. Visual software tools inform operational decision-making, optimize logistics workflows, and enhance supply chain efficiency.

## Pursuing Continuous Education

Maintaining relevant terminology as new jargon enters the field requires ongoing learning. Reading industry publications keeps you informed of shifting terminology. Participating in conventions, conferences, seminars, trade shows, workshops, and webinars connects technical concepts to operational practice.

Formal education options include online classes, employer-sponsored training, and tuition stipends. Professional certifications build specialized knowledge in blockchain technology, robotic process automation (RPA), and the Internet of Things (IoT). Industry credentials like the Certified Supply Chain Professional (CSCP) and Certified in Logistics, Transportation, and Distribution (CLTD) demonstrate verified expertise. For professionals holding a bachelor's degree in Supply Chain Management, Business Management, or related fields, pursuing an MBA focused on logistics or a Master's degree in Supply Chain Management expands career knowledge and opens lucrative positions.

## Building Professional Networks

Attending industry events and classes provides opportunities to connect with peers. Following up with new contacts on LinkedIn keeps those professional relationships active.

Joining industry associations offers structured engagement. Organizations like the Institute for Supply Management (ISM) and the Counsel of Supply Chain Management Professionals (CSCMP) offer direct access to broader professional networks.

## Developing Operational Flexibility

In science fiction, a conquering alien species stays effective by adapting quickly to changing circumstances. Developing a similar level of flexibility protects your career as new techniques replace old habits.

Cultivating a growth mindset helps you treat operational challenges as learning opportunities instead of setbacks. Regular practice in troubleshooting and problem-solving builds the practical resilience needed to manage freight calculation updates, CO2 footprint reduction requirements, and shifting supply chain demands. Keeping your resume current records these professional achievements as your career moves forward.
"""

def analyze():
    full_text = f"{title}\n{meta_title}\n{meta_desc}\n{body}"
    
    print("--- DETAILED CHECK ---")
    
    # 1. Dash Check
    dashes = ['—', '–', '--']
    dash_matches = [d for d in dashes if d in full_text]
    print(f"1. Forbidden Dashes ('—', '–', '--'): {len(dash_matches)} found. Matches: {dash_matches}")

    # 2. Banned Words Check
    banned = [
        "delve", "tapestry", "beacon", "testament", "crucial", "pivotal",
        "game-changer", "seamless", "ever-evolving", "paramount", "foster",
        "unlock", "harness", "empower", "spearhead", "robust", "demystify",
        "revolutionize", "cutting-edge", "realm"
    ]
    banned_matches = []
    for b in banned:
        matches = re.findall(r'\b' + re.escape(b) + r'\b', full_text, re.I)
        if matches:
            banned_matches.append((b, len(matches)))
    print(f"2. Banned AI Words: {len(banned_matches)} found. Matches: {banned_matches}")

    # 3. Explicit Connectors
    conn = ["that's why", "this is because", "as a result", "consequently"]
    conn_matches = []
    for c in conn:
        m = re.findall(r'\b' + re.escape(c) + r'\b', full_text, re.I)
        if m:
            conn_matches.append((c, len(m)))
    print(f"3. Explicit Connectors: {len(conn_matches)} found. Matches: {conn_matches}")

    # 4. Cliche Transitions
    cliches = ["in conclusion", "as we have seen", "furthermore", "moreover", "let's dive into", "to sum up"]
    cliche_matches = []
    for cl in cliches:
        m = re.findall(r'\b' + re.escape(cl) + r'\b', full_text, re.I)
        if m:
            cliche_matches.append((cl, len(m)))
    print(f"4. Cliche Transitions: {len(cliche_matches)} found. Matches: {cliche_matches}")

    # 5. Contrastive Negation check
    # Check "rather than", "instead of", "not X but Y", "X, not Y"
    cn_matches = []
    for term in ["rather than", "instead of"]:
        m = re.findall(r'\b' + re.escape(term) + r'\b', full_text, re.I)
        if m:
            cn_matches.extend(m)
    cn_comma_not = re.findall(r',\s*not\b', full_text, re.I)
    print(f"5. Contrastive Negations ('rather than', 'instead of', ', not'): {len(cn_matches) + len(cn_comma_not)} found -> {cn_matches + cn_comma_not}")

    # 6. Paragraph sentence counts
    paragraphs = [p.strip() for p in body.split('\n\n') if p.strip()]
    print("\n6. Paragraph sentence counts:")
    for idx, p in enumerate(paragraphs):
        if p.startswith('##'):
            continue
        # Split paragraph into lines or bullet points
        lines = [line.strip() for line in p.split('\n') if line.strip()]
        for l_idx, line in enumerate(lines):
            # sentence count
            sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', line) if s.strip()]
            print(f"   P{idx+1}-L{l_idx+1} ({len(sents)} sents): \"{line[:60]}...\"")

    # 7. Sentence Blueprint Check (Consecutive sentences starting with same word / structure)
    print("\n7. Checking consecutive sentence beginnings:")
    all_sentences = []
    for p in body.split('\n'):
        line = p.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('*'):
            line = line[1:].strip()
        sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', line) if s.strip()]
        all_sentences.extend(sents)
    
    for i in range(len(all_sentences) - 1):
        s1 = all_sentences[i]
        s2 = all_sentences[i+1]
        w1 = s1.split()[0].lower() if s1.split() else ""
        w2 = s2.split()[0].lower() if s2.split() else ""
        if w1 == w2:
            print(f"   WARNING: Consecutive sentences start with '{w1}':\n     1: {s1}\n     2: {s2}")

    # 8. Character counts
    print(f"\n8. Character lengths:")
    print(f"   H1 Title: {len(title)} chars (limit: 60) -> {'OK' if len(title) <= 60 else 'EXCEEDED'}")
    print(f"   Meta Title: {len(meta_title)} chars (limit: 60) -> {'OK' if len(meta_title) <= 60 else 'EXCEEDED'}")
    print(f"   Meta Description: {len(meta_desc)} chars (limit: 155) -> {'OK' if len(meta_desc) <= 155 else 'EXCEEDED'}")

analyze()
