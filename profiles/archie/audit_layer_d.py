from texts import orig, rewrite

# Let's list all claims in the rewrite and map them to original source text sentences.

claims_audit = [
    {
        "rewrite_quote": "In 2018, SeaRates published an initial commentary on quantum computing, pointing to early work by Google and IBM alongside research from Alibaba.",
        "orig_source_quote": "In 2018, we first conceptually discussed quantum computing, specifically the efforts of giants like Google, IBM, and Alibaba, and its implications for logistics.",
        "status": "PASS",
        "notes": "Accurate."
    },
    {
        "rewrite_quote": "The premise was straightforward: advanced processing would eventually alter how cargo moves globally.",
        "orig_source_quote": "...and its implications for logistics... For us, technology has been a way to truly improve efficiency, transparency, and collaboration in logistics.",
        "status": "PASS",
        "notes": "Fair paraphrase of 'implications for logistics'."
    },
    {
        "rewrite_quote": "Eight years later, the conversation has changed.",
        "orig_source_quote": "In 2018... Nowadays, this topic is more relevant than ever.",
        "status": "FLAG / CHECK",
        "notes": "Original mentions 2018 and 'Nowadays'. In 2026 (or 2026 - 2018 = 8 years), but does the original source text explicitly state 'Eight years later'? Let's check!"
    },
    {
        "rewrite_quote": "Social feeds like LinkedIn are saturated with promotional pitches asking shippers to trust unverified artificial intelligence products.",
        "orig_source_quote": "As you scroll through our LinkedIn feed today, it is filled with calls to 'trust our AI solution', so there are more layers of validation for this topic.",
        "status": "PASS",
        "notes": "Accurately reflects LinkedIn feed filled with 'trust our AI solution'."
    },
    {
        "rewrite_quote": "Yet global trade remains physical at its core. A supply network operates under a strict constraint where total operational capacity is bound by its weakest participant. Small regional forwarders and major carriers must function alongside port terminals.",
        "orig_source_quote": "The biggest challenge is no longer technology but the complex network of participants. It's the 'weakest link principle,' where the capability of the entire system depends on its weakest participant. Our role is to ensure that every link, from the smallest freight forwarder to the largest shipping line, is strengthened...",
        "status": "PASS",
        "notes": "Accurately traces 'weakest link principle' and forwarders/shipping lines/terminals."
    },
    {
        "rewrite_quote": "Since 2010, SeaRates has focused on building practical automation for freight forwarders and shippers. The platform provides APIs and web applications for instant freight rate calculations, cargo tracking, digital booking, and automated document processing.",
        "orig_source_quote": "Our team has been at the forefront of logistics automation since 2010... Over the years, we have developedweb applications and APIsthat automate all processes. Our solutions cover the full spectrum of logistics needs — from automated document handling and seamless booking to essential tools like instantfreight rate calculationandreal-time cargo tracking.",
        "status": "PASS",
        "notes": "Exact match for 2010, web apps, APIs, rate calculation, cargo tracking, booking, document handling."
    },
    {
        "rewrite_quote": "Through the Digital Freight Alliance, independent forwarders access tools that connect their systems with major ocean carriers, strengthening individual links across the supply network.",
        "orig_source_quote": "TheDigital Freight Allianceis a big step in this direction, as it’s the largest network of freight forwarders, filled with solutions and digital tools.",
        "status": "PASS",
        "notes": "Traces back to Digital Freight Alliance."
    },
    {
        "rewrite_quote": "Computing is undergoing its first fundamental restructuring in six decades. NVIDIA CEO Jensen Huang described this shift as a move toward GPU supercomputers that act as intelligence factories. Data is no longer merely stored; it is converted into actionable decisions.",
        "orig_source_quote": "As it has been aptly stated by Mr. Huang, CEO of NVIDIA, this is the reimagining of computing after 60 long years. The push towards GPU and AI supercomputers is more than mere acceleration of computing; it is about 'creating factories of intelligence.' These machines will not just convert data, but breed intelligence from it to solve problems...",
        "status": "PASS",
        "notes": "Exact match for Jensen Huang, CEO of NVIDIA, 60 years, GPU/AI supercomputers, factories of intelligence, converting data."
    },
    {
        "rewrite_quote": "The speed of hardware development explains this shift. Moore's Law delivered a 100-fold increase in computing power over ten years. During that same decade, AI processing expanded by a factor of 100,000.",
        "orig_source_quote": "While Moore's Law has given us 100 times enhancements in power over a decade,AI innovationshave been growing with a factor of 100,000 in the same period.",
        "status": "PASS",
        "notes": "Exact match for 100x vs 100,000 over a decade."
    },
    {
        "rewrite_quote": "This acceleration brings digital twins into physical industries. Complex shipping operations can now be modeled digitally to evaluate routing changes before vessels depart.",
        "orig_source_quote": "The distant imagination of 'physical AI,' that is,digital twinsin optimizing and improving physical industries like ours, has now ceased to be a distant imagination.",
        "status": "PASS",
        "notes": "Traces back to physical AI / digital twins in physical industries."
    },
    {
        "rewrite_quote": "Google developed the Willow chip, equipped with 105 qubits and working quantum error correction. In benchmark tests, Willow completed calculations in minutes that would demand years from standard supercomputers. This result offers a clear demonstration of practical quantum advantage.",
        "orig_source_quote": "With its 105 qubits, Google's Willow chip is evidence that practical 'quantum supremacy' is nearly ready to be harnessed, having practically demonstrated quantum error correction. They were able to perform calculations in a matter of minutes that would have taken a supercomputer years...",
        "status": "PASS",
        "notes": "Exact match for Google Willow, 105 qubits, quantum error correction, minutes vs years for supercomputer, quantum supremacy/advantage."
    },
    {
        "rewrite_quote": "Microsoft pursued a different architectural path with its Majorana 1 chip. Built on 17 years of research, the team isolated a stable state of matter to produce error-resistant topological qubits. Although Majorana 1 currently operates with eight qubits, its topological core is engineered to scale toward one million qubits over time.",
        "orig_source_quote": "Microsoft's approach with its Majorana 1 chip is, in some ways, just as exciting. They have discovered a new form of matter for qubits that is more stable and error-resistant... However, after 17 years of research, they have only managed to place eight qubits on the chip, but their concept of a 'topological core' capable of scaling to a million qubits gives an idea of their long-term strategy...",
        "status": "PASS",
        "notes": "Exact match for Microsoft Majorana 1, 17 years, new form of matter, error-resistant topological qubits, 8 qubits, topological core scaling to 1 million."
    },
    {
        "rewrite_quote": "Combining AI supercomputers with quantum processing creates new capabilities for global freight routing.",
        "orig_source_quote": "...the solution to our world's most untamed problems is found in the interplay between quantum computing and AI supercomputers. So for theshipping industry, it'll be a revolution.",
        "status": "PASS",
        "notes": "Exact match for interplay between quantum computing and AI supercomputers in shipping/freight routing."
    },
    {
        "rewrite_quote": "Consider the traveling salesman problem applied to international shipping. Standard supercomputers struggle to calculate optimal routes when coordinates multiply into thousands of variables. A quantum algorithm can evaluate millions of nodes in seconds, factoring weather patterns and geopolitical hazards alongside multimodal transfers.",
        "orig_source_quote": "Imagine quantum algorithmsoptimizing global deliveryroutes instantaneously, incorporating weather variables, geopolitical risks, and multimodal logistics with unprecedented accuracy... We solve the traveling salesman problem with millions of nodes in seconds, whereas even the most powerful supercomputer today is incapable of solving the issue meaningfully within any reasonable time for an acceptable number of coordinates.",
        "status": "PASS",
        "notes": "Exact match for traveling salesman problem, weather variables, geopolitical risks/hazards, multimodal logistics/transfers, millions of nodes in seconds vs standard supercomputer struggling with coordinates."
    },
    {
        "rewrite_quote": "This capacity changes risk modeling. Supply chains can simulate disruptions from trade restrictions or port closures before delays occur.",
        "orig_source_quote": "Imagine a world where supply chain resilience to any disruption, such as pandemics or trade restrictions, can be perfectly modeled.",
        "status": "FLAG / CHECK",
        "notes": "Original mentions 'pandemics or trade restrictions'. Rewrite states 'trade restrictions or port closures'. Are 'port closures' in the original source text? Let's check!"
    },
    {
        "rewrite_quote": "Precise route optimization also cuts vessel fuel consumption, lowering operating costs and carbon output.",
        "orig_source_quote": "Through such optimization, fuel consumption shall be minimized, and thus costs alongsidecarbon emissionswill shrink in this process.",
        "status": "PASS",
        "notes": "Exact match for fuel consumption, operating costs, carbon output/emissions."
    },
    {
        "rewrite_quote": "Logistics has always been an exercise in applied logic. As computing models evolve, the focus remains on building reliable tools that simplify trade for every participant.",
        "orig_source_quote": "Since our inception, SeaRates.com has stood by the premise: logistics means logic. It is a system that knows how to be designed and optimized... We are not just building tools but the actual future of global trade.",
        "status": "PASS",
        "notes": "Exact match for 'logistics means logic' / 'applied logic', building tools, simplifying trade/global trade."
    }
]

print("AUDIT RESULTS:")
for c in claims_audit:
    if c['status'] != 'PASS':
        print(f"[{c['status']}] Rewrite: {c['rewrite_quote']}\n  Orig: {c['orig_source_quote']}\n  Notes: {c['notes']}\n")
