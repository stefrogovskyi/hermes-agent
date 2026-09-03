import re

new_title = "Lockout Tagout Compliance for Multinational Fleet Safety"
meta_title = "Lockout Tagout Protocols for Global Fleet Compliance"
meta_desc = "Secure fleet maintenance using LOTO protocols. Comply with OSHA and HSE standards, isolate stored energy, and protect transport operations from downtime."

body = """Unplanned machinery activation during routine maintenance endangers technicians and halts freight movement. When transport equipment starts unexpectedly, technicians face electrocution, severe injury, or death. Implementing lockout and tagout protocols neutralizes these hazards, creating a protected workplace while keeping transit schedules on track.

### Energy Isolation Mechanisms

Preventing accidental energy release requires complete isolation across all operational systems. Equipment maintenance involves five primary energy forms: hydraulic, mechanical, thermal, electrical, and pneumatic. Specialized lockout tagout kits contain physical tools to neutralize extreme temperatures, secure moving parts, de-energize electrical circuits, and seal valves. Using these kits prevents machine damage, eliminates unexpected energy discharges, and stops costly production downtime before it starts.

### Hardware Devices and Physical Controls

Safety enforcement relies on two physical devices: lockout tools and tagout indicators. 

Lockout devices secure energy isolation devices in safe or off positions. Using padlocks, lockout hasps, and dedicated tags, maintenance personnel physically block switches and controls. This mechanical barrier prevents the unintentional activation of fleet machinery and transport assets.

Tagout devices serve as durable visual warnings attached directly to lockout hardware. These labels state that energy isolation is active, displaying the reason for the procedure, its expected duration, and the name of the technician executing the work.

### The Isolation Sequence

The energy isolation procedure follows a clear sequence. Before touching any machinery, technicians identify every connected energy source. Shutting down the equipment occurs next through designated controls and switches. Applying physical locks and tags directly to isolation devices prevents inadvertent re-energization during maintenance.

Completing this process allows personnel to service and maintain transport assets safely, supporting efficient logistics operations.

### Regulatory Compliance and Auditing Standards

Regulatory authorities enforce strict mandates to safeguard workforce safety. In the United States, the Occupational Safety and Health Administration (OSHA) sets these legal requirements, while the Health and Safety Executive (HSE) governs compliance across the United Kingdom.

Organizations must develop and implement written lockout/tagout procedures. Compliance requires comprehensive training for staff directly affected by LOTO protocols as well as technicians performing physical lockouts. Regulators also mandate regular auditing and inspections. Facilities must verify that all isolation equipment remains up-to-date and suitable for effective energy control.

### Operational and Financial Consequences

Neglecting lockout and tagout standards exposes transport companies to severe operational and financial liabilities. 

Individual employees face potential legal liabilities following safety failures. For the organization, non-compliance triggers steep fines and regulatory penalties that inflate transportation budgets. Workplace injuries lead to substantial medical expenses, covering emergency treatment, hospitalization, and long-term rehabilitation.

Beyond direct financial payouts, equipment accidents trigger production downtime and schedule delays across supply networks. Incidents damage corporate reputation, eroding trust among investors, customers, regulatory agencies, and key stakeholders.

### Strategic Integration for Logistics Leaders

Although operational managers often view lockout/tagout protocols as a burdensome administrative delay, physical compliance forms the foundation of an incident-free, efficient workplace.

Proper LOTO kits give operators the physical tools needed to meet OSHA and HSE standards, preventing casualties and equipment damage. Establishing strict energy isolation compliance enables leadership to focus on digital logistics optimization and securing favorable freight rates."""

full_text = f"{new_title}\n{meta_title}\n{meta_desc}\n{body}"

print("Length of new_title:", len(new_title))
print("Length of meta_title:", len(meta_title))
print("Length of meta_desc:", len(meta_desc))

# Check Rule 1: em-dashes
if "—" in full_text or "--" in full_text:
    print("FAIL: em-dash found")
else:
    print("PASS: No em-dashes")

# Check Rule 2: AI clichés
cliches = [
    r"\bcrucial role\b", r"\bdelve\b", r"it is not just .*, it is", r"\bin conclusion\b",
    r"\bin today's world\b", r"\bvital asset\b", r"\bseamlessly\b", r"\bgame-changer\b",
    r"\btestament to\b", r"\bbeacon\b", r"\bdive into\b", r"\bimportant to note\b"
]
found_cliches = [c for c in cliches if re.search(c, full_text, re.IGNORECASE)]
print("Clichés found:", found_cliches)

# Check Rule 5: Connectors
connectors = [
    r"\bfurthermore\b", r"\bmoreover\b", r"\bin addition\b", r"\bconsequently\b",
    r"\bimportantly\b", r"\bhowever\b"
]
found_conn = [c for c in connectors if re.search(c, full_text, re.IGNORECASE)]
print("Connectors found:", found_conn)

# Rule 6: Contrastive negation
# e.g., "not X, but Y", "not X, Y", "not only X but Y"
cn = re.findall(r"\bnot\b.*?\bbut\b", full_text, re.IGNORECASE)
print("Contrastive negations:", cn)

# Rule 9: Symmetric Antithesis
# e.g. "while X does A, Y does B"
# Let's inspect sentences with 'while', 'whereas', 'not only... but also'
antithesis = re.findall(r"\bwhile\b.*?,", full_text, re.IGNORECASE)
print("While clauses:", antithesis)

