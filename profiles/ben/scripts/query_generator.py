import random

SERVICES = [
    "mobile auto repair", "mobile mechanic", "mobile car detailing", "mobile tire repair",
    "emergency towing service", "auto body paint shop", "roofing contractor", "roof repair service",
    "ac repair and hvac", "emergency plumber", "licensed electrician", "tree service and removal",
    "pressure washing service", "residential painter", "handyman service", "24 hour locksmith",
    "pool maintenance and repair", "carpet cleaning service", "junk removal hauling", "fence contractor"
]

CITIES = [
    "Miami FL", "Orlando FL", "Tampa FL", "Fort Lauderdale FL", "Jacksonville FL",
    "Houston TX", "Dallas TX", "Austin TX", "San Antonio TX", "Fort Worth TX",
    "Atlanta GA", "Phoenix AZ", "Scottsdale AZ", "Tucson AZ", "Las Vegas NV",
    "Denver CO", "Charlotte NC", "Raleigh NC", "Nashville TN", "Chicago IL",
    "Boston MA", "Philadelphia PA", "Los Angeles CA", "San Diego CA", "Sacramento CA"
]

def get_dynamic_queries():
    queries = []
    for s in SERVICES:
        for c in CITIES:
            niche_name = s.title()
            query_str = f"{s} in {c}"
            queries.append((niche_name, c, query_str))
    random.shuffle(queries)
    return queries

if __name__ == "__main__":
    q = get_dynamic_queries()
    print(f"Total dynamic query combinations: {len(q)}")
    print("Sample:", q[:5])
