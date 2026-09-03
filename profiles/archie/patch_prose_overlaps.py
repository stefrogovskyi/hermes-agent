with open("/opt/hermes/profiles/archie/final_checked_rewrite.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Replace 1
old1 = "You can also adjust the number of allowed layers or enter specific limits into the \"Mass\" or \"Height\" fields."
new1 = "Users can also modify maximum layer limits or set custom parameters within the \"Mass\" and \"Height\" fields."

# Replace 2
old2 = "We added new transportation modes for Land FTL requests within Request a Quote and Quick Request quote tools."
new2 = "Additional transport modes for Land FTL inquiries were introduced across both Request a Quote and Quick Request quote forms."

text = text.replace(old1, new1)
text = text.replace(old2, new2)

with open("/opt/hermes/profiles/archie/final_checked_rewrite.txt", "w", encoding="utf-8") as f:
    f.write(text)

print("Replacement complete.")
