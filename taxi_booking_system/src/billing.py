from utils import calculate_distance, RATES


def calculate_fare():
    """Compute fare without booking"""
    origin = input("Origin address: ")
    destination = input("Destination address: ")
    print("Categories:", ", ".join(RATES.keys()))
    category = input("Choose category: ")
    if category not in RATES:
        print("❌  Invalid category.")
        return
    dist = calculate_distance(origin, destination)
    if dist is None:
        print("❌  Invalid addresses.")
        return
    fare = dist * RATES[category]
    print(f"🛣️  Distance: {dist:.2f} km, 💵 Fare: {fare:.2f} SAR")