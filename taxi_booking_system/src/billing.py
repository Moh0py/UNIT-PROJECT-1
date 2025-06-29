def calculate_fare(distance: int, rate: int = 2) -> int:
    return distance * rate + (0.15 * distance)

def print_receipt(user: dict, ride: dict):
    cost = calculate_fare(ride['distance'])
    print("--- Receipt ---")
    print(f"User:        {user['username']}")
    print(f"From → To:   {ride['origin']} → {ride['destination']}")
    print(f"Distance:    {ride['distance']} km")
    print(f"Total Cost:  {cost} SAR")
    print()
