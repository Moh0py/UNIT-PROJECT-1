# def add_vat(cost: int) -> int:
#     vat = cost * 0.15
#     return round(cost + vat, 2)


def calculate_fare(distance: int, rate: int = 2) -> int:

    return distance * rate

def print_receipt(user: dict, ride: dict):
    cost = calculate_fare(ride['distance'])
    print("--- Receipt ---")
    print(f"User:        {user['username']}")
    print(f"From → To:   {ride['origin']} → {ride['destination']}")
    print(f"Distance:    {ride['distance']} km")
    print(f"Total Cost:  {cost} SAR")
    print("----------------\n")
